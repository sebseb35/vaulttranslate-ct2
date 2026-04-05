from __future__ import annotations

import logging
from importlib import import_module
from collections.abc import Callable
from typing import Any

from packages.core import Segment, TranslationRequest, TranslationResult, TranslatorEngine

logger = logging.getLogger(__name__)


class CTranslate2EngineError(RuntimeError):
    """Raised when the CTranslate2 engine cannot initialize or translate."""


def _load_ctranslate2() -> Any:
    return import_module("ctranslate2")


class CTranslate2TranslatorEngine(TranslatorEngine):
    def __init__(
        self,
        model_path: str,
        *,
        inter_threads: int = 1,
        intra_threads: int = 1,
        compute_type: str = "default",
        tokenizer: Callable[[str], list[str]] | None = None,
        detokenizer: Callable[[list[str]], str] | None = None,
    ) -> None:
        if not model_path.strip():
            raise ValueError("model_path must be a non-empty string")
        if inter_threads < 1:
            raise ValueError("inter_threads must be >= 1")
        if intra_threads < 1:
            raise ValueError("intra_threads must be >= 1")

        self._model_path = model_path
        self._tokenizer = tokenizer or self._default_tokenizer
        self._detokenizer = detokenizer or self._default_detokenizer

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
        batch_tokens = [self._tokenizer(segment.text) for segment in request.segments]

        logger.debug("Translating %d segments with CTranslate2", len(batch_tokens))

        try:
            raw_results = self._translator.translate_batch(batch_tokens)
        except Exception as exc:
            logger.error("CTranslate2 batch translation failed: %s", exc)
            raise CTranslate2EngineError(f"CTranslate2 batch translation failed: {exc}") from exc

        if len(raw_results) != len(request.segments):
            raise CTranslate2EngineError(
                "CTranslate2 returned a different number of results than requested segments"
            )

        translated_segments: list[Segment] = []
        for source_segment, result in zip(request.segments, raw_results, strict=True):
            hypotheses = getattr(result, "hypotheses", None)
            if not hypotheses or not hypotheses[0]:
                raise CTranslate2EngineError(
                    f"Empty translation hypothesis for segment '{source_segment.segment_id}'"
                )

            best_tokens = hypotheses[0]
            translated_text = self._detokenizer(best_tokens)
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
            },
        )

    @staticmethod
    def _default_tokenizer(text: str) -> list[str]:
        """Fallback tokenizer for tests and simple demos only."""
        stripped = text.strip()
        if not stripped:
            return [""]
        return stripped.split()

    @staticmethod
    def _default_detokenizer(tokens: list[str]) -> str:
        """Fallback detokenizer for tests and simple demos only."""
        if len(tokens) == 1 and tokens[0] == "":
            return ""
        return " ".join(tokens)
