from __future__ import annotations

import logging
from collections.abc import Callable
from importlib import import_module
import re
from typing import Any

from packages.core import Segment, TranslationRequest, TranslationResult, TranslatorEngine

logger = logging.getLogger(__name__)
_NEWLINE_SPLIT_PATTERN = re.compile(r"(\n+)")


class CTranslate2EngineError(RuntimeError):
    """Raised when the CTranslate2 engine cannot initialize or translate."""


def _load_ctranslate2() -> Any:
    return import_module("ctranslate2")


def _load_transformers() -> Any:
    return import_module("transformers")


class CTranslate2TranslatorEngine(TranslatorEngine):
    def __init__(
        self,
        model_path: str,
        *,
        tokenizer_path: str | None = None,
        inter_threads: int = 1,
        intra_threads: int = 1,
        compute_type: str = "default",
        tokenizer: Any | None = None,
        token_encoder: Callable[[Any, str], list[str]] | None = None,
        token_decoder: Callable[[Any, list[str]], str] | None = None,
    ) -> None:
        if not model_path.strip():
            raise ValueError("model_path must be a non-empty string")
        if inter_threads < 1:
            raise ValueError("inter_threads must be >= 1")
        if intra_threads < 1:
            raise ValueError("intra_threads must be >= 1")

        self._model_path = model_path
        self._tokenizer_path = tokenizer_path or model_path
        self._tokenizer = tokenizer
        self._token_encoder = token_encoder or self._encode_with_tokenizer
        self._token_decoder = token_decoder or self._decode_with_tokenizer

        if self._tokenizer is None:
            try:
                transformers = _load_transformers()
                self._tokenizer = transformers.AutoTokenizer.from_pretrained(
                    self._tokenizer_path,
                    local_files_only=True,
                )
            except Exception as exc:
                logger.error("Failed to load tokenizer from '%s': %s", self._tokenizer_path, exc)
                raise CTranslate2EngineError(
                    f"Failed to load tokenizer from '{self._tokenizer_path}': {exc}"
                ) from exc

        try:
            ctranslate2 = _load_ctranslate2()
            self._translator = ctranslate2.Translator(
                model_path,
                device="cpu",
                inter_threads=inter_threads,
                intra_threads=intra_threads,
                compute_type=compute_type,
            )
        except Exception as exc:  # pragma: no cover - exercised by mocked error tests
            logger.error("Failed to initialize CTranslate2 translator: %s", exc)
            raise CTranslate2EngineError(f"Failed to initialize CTranslate2 translator: {exc}") from exc

    def translate(self, request: TranslationRequest) -> TranslationResult:
        prepared_segments: list[list[str]] = []
        chunk_index_to_segment: list[tuple[int, int]] = []
        batch_tokens: list[list[str]] = []

        for segment_idx, segment in enumerate(request.segments):
            chunks = _split_preserving_newlines(segment.text)
            prepared_segments.append(chunks)
            for chunk_idx, chunk in enumerate(chunks):
                if not _is_translatable_chunk(chunk):
                    continue
                chunk_index_to_segment.append((segment_idx, chunk_idx))
                batch_tokens.append(self._token_encoder(self._tokenizer, chunk))

        logger.debug("Translating %d segments with CTranslate2", len(batch_tokens))

        raw_results: list[Any] = []
        if batch_tokens:
            try:
                raw_results = self._translator.translate_batch(batch_tokens)
            except Exception as exc:
                logger.error("CTranslate2 batch translation failed: %s", exc)
                raise CTranslate2EngineError(f"CTranslate2 batch translation failed: {exc}") from exc

        if len(raw_results) != len(chunk_index_to_segment):
            raise CTranslate2EngineError(
                "CTranslate2 returned a different number of results than requested segments"
            )

        translated_chunk_texts: dict[tuple[int, int], str] = {}
        for mapping, result in zip(chunk_index_to_segment, raw_results, strict=True):
            hypotheses = getattr(result, "hypotheses", None)
            if not hypotheses or not hypotheses[0]:
                raise CTranslate2EngineError("Empty translation hypothesis in chunked translation")
            best_tokens = hypotheses[0]
            translated_chunk_texts[mapping] = self._token_decoder(self._tokenizer, best_tokens)

        translated_segments: list[Segment] = []
        for segment_idx, source_segment in enumerate(request.segments):
            chunks = prepared_segments[segment_idx]
            rebuilt_parts: list[str] = []
            for chunk_idx, chunk in enumerate(chunks):
                rebuilt_parts.append(translated_chunk_texts.get((segment_idx, chunk_idx), chunk))
            translated_text = "".join(rebuilt_parts)
            translated_segments.append(
                Segment(
                    segment_id=source_segment.segment_id,
                    text=translated_text,
                    constraints=source_segment.constraints,
                )
            )

        return TranslationResult(
            document_format=request.document_format,
            source_language=request.source_language,
            target_language=request.target_language,
            translated_segments=tuple(translated_segments),
            metadata={
                **request.metadata,
                "engine": "ctranslate2",
                "model_path": self._model_path,
                "tokenizer_path": self._tokenizer_path,
            },
        )

    @staticmethod
    def _encode_with_tokenizer(tokenizer: Any, text: str) -> list[str]:
        token_ids = tokenizer.encode(text, add_special_tokens=True)
        token_strings = tokenizer.convert_ids_to_tokens(token_ids)
        return [str(token) for token in token_strings]

    @staticmethod
    def _decode_with_tokenizer(tokenizer: Any, tokens: list[str]) -> str:
        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        return str(tokenizer.decode(token_ids, skip_special_tokens=True))


def _split_preserving_newlines(text: str) -> list[str]:
    if text == "":
        return [""]
    return _NEWLINE_SPLIT_PATTERN.split(text)


def _is_translatable_chunk(chunk: str) -> bool:
    return chunk != "" and "\n" not in chunk and not chunk.isspace()
