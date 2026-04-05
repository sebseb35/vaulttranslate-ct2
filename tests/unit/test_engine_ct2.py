from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

import pytest

from packages.core.models import DocumentFormat, Segment, TranslationRequest
from packages.engine_ct2 import CTranslate2EngineError, CTranslate2TranslatorEngine


def _request(*, segments: tuple[Segment, ...]) -> TranslationRequest:
    return TranslationRequest(
        document_format=DocumentFormat.TXT,
        source_language="en",
        target_language="fr",
        segments=segments,
    )


@dataclass
class _CallCapture:
    model_path: str | None = None
    device: str | None = None
    inter_threads: int | None = None
    intra_threads: int | None = None
    compute_type: str | None = None
    batch_source: list[list[str]] | None = None


class _FakeTranslationResult:
    def __init__(self, tokens: list[str]) -> None:
        self.hypotheses = [tokens]


class _FakeAutoTokenizer:
    def __init__(self) -> None:
        self._id_to_token = {
            101: "<s>",
            102: "</s>",
            201: "hello",
            202: "world",
            203: "how",
            204: "are",
            205: "you",
            206: "this",
            207: "is",
            208: "a",
            209: "plain",
            210: "text",
            211: "file",
            212: ".",
            301: "bonjour",
            302: "monde",
            303: "comment",
            304: "ca",
            305: "va",
            306: "c",
            307: "'",
            308: "est",
            309: "un",
            310: "fichier",
            311: "texte",
        }
        self._token_to_id = {token: token_id for token_id, token in self._id_to_token.items()}
        self.encode_calls: list[str] = []
        self.decode_calls: list[list[int]] = []

    def encode(self, text: str, add_special_tokens: bool = True) -> list[int]:
        self.encode_calls.append(text)
        words = text.split()
        ids = [self._token_to_id[word] for word in words]
        if add_special_tokens:
            return [101, *ids, 102]
        return ids

    def convert_ids_to_tokens(self, token_ids: list[int]) -> list[str]:
        return [self._id_to_token[token_id] for token_id in token_ids]

    def convert_tokens_to_ids(self, tokens: list[str]) -> list[int]:
        return [self._token_to_id[token] for token in tokens]

    def decode(self, token_ids: list[int], skip_special_tokens: bool = True) -> str:
        self.decode_calls.append(token_ids)
        tokens = self.convert_ids_to_tokens(token_ids)
        if skip_special_tokens:
            tokens = [token for token in tokens if token not in {"<s>", "</s>"}]
        return " ".join(tokens)


def _patch_transformers(
    monkeypatch: pytest.MonkeyPatch,
    *,
    tokenizer: _FakeAutoTokenizer | None = None,
    capture: dict[str, Any] | None = None,
) -> _FakeAutoTokenizer:
    fake_tokenizer = tokenizer or _FakeAutoTokenizer()

    class _FakeAutoTokenizerFactory:
        @staticmethod
        def from_pretrained(path: str, local_files_only: bool) -> _FakeAutoTokenizer:
            if capture is not None:
                capture["tokenizer_path"] = path
                capture["local_files_only"] = local_files_only
            return fake_tokenizer

    fake_transformers_module = SimpleNamespace(AutoTokenizer=_FakeAutoTokenizerFactory)
    monkeypatch.setattr(
        "packages.engine_ct2.engine._load_transformers",
        lambda: fake_transformers_module,
    )
    return fake_tokenizer


def test_engine_initializes_ctranslate2_translator_with_cpu_threads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    capture = _CallCapture()
    tokenizer_capture: dict[str, Any] = {}
    _patch_transformers(monkeypatch, capture=tokenizer_capture)

    class _FakeTranslator:
        def __init__(
            self,
            model_path: str,
            device: str,
            inter_threads: int,
            intra_threads: int,
            compute_type: str,
        ) -> None:
            capture.model_path = model_path
            capture.device = device
            capture.inter_threads = inter_threads
            capture.intra_threads = intra_threads
            capture.compute_type = compute_type

        def translate_batch(self, source: list[list[str]]) -> list[_FakeTranslationResult]:
            capture.batch_source = source
            return [_FakeTranslationResult(["<s>", "bonjour", "</s>"])]

    fake_ct2_module = SimpleNamespace(Translator=_FakeTranslator)
    monkeypatch.setattr("packages.engine_ct2.engine._load_ctranslate2", lambda: fake_ct2_module)

    engine = CTranslate2TranslatorEngine(
        model_path="/models/ct2-en-fr",
        inter_threads=2,
        intra_threads=4,
        compute_type="int8",
    )

    result = engine.translate(_request(segments=(Segment(segment_id="s1", text="hello"),)))

    assert capture.model_path == "/models/ct2-en-fr"
    assert capture.device == "cpu"
    assert capture.inter_threads == 2
    assert capture.intra_threads == 4
    assert capture.compute_type == "int8"
    assert tokenizer_capture == {
        "tokenizer_path": "/models/ct2-en-fr",
        "local_files_only": True,
    }
    assert capture.batch_source == [["<s>", "hello", "</s>"]]
    assert result.translated_segments == (Segment(segment_id="s1", text="bonjour"),)


def test_engine_uses_tokenizer_path_when_provided(monkeypatch: pytest.MonkeyPatch) -> None:
    tokenizer_capture: dict[str, Any] = {}
    _patch_transformers(monkeypatch, capture=tokenizer_capture)

    class _FakeTranslator:
        def __init__(
            self,
            model_path: str,
            device: str,
            inter_threads: int,
            intra_threads: int,
            compute_type: str,
        ) -> None:
            del model_path, device, inter_threads, intra_threads, compute_type

        def translate_batch(self, source: list[list[str]]) -> list[_FakeTranslationResult]:
            del source
            return [_FakeTranslationResult(["<s>", "bonjour", "</s>"])]

    fake_ct2_module = SimpleNamespace(Translator=_FakeTranslator)
    monkeypatch.setattr("packages.engine_ct2.engine._load_ctranslate2", lambda: fake_ct2_module)

    engine = CTranslate2TranslatorEngine(
        model_path="/models/ct2-en-fr",
        tokenizer_path="/tokenizers/marian-en-fr",
    )
    engine.translate(_request(segments=(Segment(segment_id="s1", text="hello"),)))

    assert tokenizer_capture == {
        "tokenizer_path": "/tokenizers/marian-en-fr",
        "local_files_only": True,
    }


def test_engine_translates_segment_batch_preserving_order_and_ids(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_transformers(monkeypatch)

    class _FakeTranslator:
        def __init__(
            self,
            model_path: str,
            device: str,
            inter_threads: int,
            intra_threads: int,
            compute_type: str,
        ) -> None:
            del model_path, device, inter_threads, intra_threads, compute_type

        def translate_batch(self, source: list[list[str]]) -> list[_FakeTranslationResult]:
            assert source == [
                ["<s>", "hello", "world", "</s>"],
                ["<s>", "how", "are", "you", "</s>"],
            ]
            return [
                _FakeTranslationResult(["<s>", "bonjour", "monde", "</s>"]),
                _FakeTranslationResult(["<s>", "comment", "ca", "va", "</s>"]),
            ]

    fake_ct2_module = SimpleNamespace(Translator=_FakeTranslator)
    monkeypatch.setattr("packages.engine_ct2.engine._load_ctranslate2", lambda: fake_ct2_module)

    engine = CTranslate2TranslatorEngine(model_path="/models/ct2-en-fr")
    request = _request(
        segments=(
            Segment(segment_id="s1", text="hello world"),
            Segment(segment_id="s2", text="how are you"),
        )
    )

    result = engine.translate(request)

    assert [segment.segment_id for segment in result.translated_segments] == ["s1", "s2"]
    assert [segment.text for segment in result.translated_segments] == [
        "bonjour monde",
        "comment ca va",
    ]


def test_engine_wraps_translation_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_transformers(monkeypatch)

    class _FakeTranslator:
        def __init__(
            self,
            model_path: str,
            device: str,
            inter_threads: int,
            intra_threads: int,
            compute_type: str,
        ) -> None:
            del model_path, device, inter_threads, intra_threads, compute_type

        def translate_batch(self, source: list[list[str]]) -> list[_FakeTranslationResult]:
            del source
            raise RuntimeError("translation backend failed")

    fake_ct2_module = SimpleNamespace(Translator=_FakeTranslator)
    monkeypatch.setattr("packages.engine_ct2.engine._load_ctranslate2", lambda: fake_ct2_module)

    engine = CTranslate2TranslatorEngine(model_path="/models/ct2-en-fr")

    with pytest.raises(CTranslate2EngineError, match="translation backend failed"):
        engine.translate(_request(segments=(Segment(segment_id="s1", text="hello"),)))


def test_engine_wraps_initialization_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_transformers(monkeypatch)

    class _FailingTranslator:
        def __init__(
            self,
            model_path: str,
            device: str,
            inter_threads: int,
            intra_threads: int,
            compute_type: str,
        ) -> None:
            del model_path, device, inter_threads, intra_threads, compute_type
            raise RuntimeError("init backend failed")

    fake_ct2_module = SimpleNamespace(Translator=_FailingTranslator)
    monkeypatch.setattr("packages.engine_ct2.engine._load_ctranslate2", lambda: fake_ct2_module)

    with pytest.raises(CTranslate2EngineError, match="init backend failed"):
        CTranslate2TranslatorEngine(model_path="/models/ct2-en-fr")


def test_engine_wraps_tokenizer_initialization_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FailingAutoTokenizerFactory:
        @staticmethod
        def from_pretrained(path: str, local_files_only: bool) -> _FakeAutoTokenizer:
            del path, local_files_only
            raise RuntimeError("tokenizer init failed")

    fake_transformers_module = SimpleNamespace(AutoTokenizer=_FailingAutoTokenizerFactory)
    monkeypatch.setattr(
        "packages.engine_ct2.engine._load_transformers",
        lambda: fake_transformers_module,
    )

    with pytest.raises(CTranslate2EngineError, match="tokenizer init failed"):
        CTranslate2TranslatorEngine(model_path="/models/ct2-en-fr")


def test_engine_rejects_result_count_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_transformers(monkeypatch)

    class _FakeTranslator:
        def __init__(
            self,
            model_path: str,
            device: str,
            inter_threads: int,
            intra_threads: int,
            compute_type: str,
        ) -> None:
            del model_path, device, inter_threads, intra_threads, compute_type

        def translate_batch(self, source: list[list[str]]) -> list[_FakeTranslationResult]:
            assert len(source) == 2
            return [_FakeTranslationResult(["<s>", "bonjour", "</s>"])]

    fake_ct2_module = SimpleNamespace(Translator=_FakeTranslator)
    monkeypatch.setattr("packages.engine_ct2.engine._load_ctranslate2", lambda: fake_ct2_module)

    engine = CTranslate2TranslatorEngine(model_path="/models/ct2-en-fr")
    request = _request(
        segments=(
            Segment(segment_id="s1", text="hello"),
            Segment(segment_id="s2", text="world"),
        )
    )

    with pytest.raises(CTranslate2EngineError, match="different number of results"):
        engine.translate(request)


def test_engine_preserves_multiline_content_with_chunked_translation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_transformers(monkeypatch)

    class _FakeTranslator:
        def __init__(
            self,
            model_path: str,
            device: str,
            inter_threads: int,
            intra_threads: int,
            compute_type: str,
        ) -> None:
            del model_path, device, inter_threads, intra_threads, compute_type

        def translate_batch(self, source: list[list[str]]) -> list[_FakeTranslationResult]:
            assert source == [
                ["<s>", "hello", "world", "</s>"],
                ["<s>", "this", "is", "a", "plain", "text", "file", "</s>"],
            ]
            return [
                _FakeTranslationResult(["<s>", "bonjour", "monde", "</s>"]),
                _FakeTranslationResult(
                    ["<s>", "c", "'", "est", "un", "fichier", "texte", "</s>"]
                ),
            ]

    fake_ct2_module = SimpleNamespace(Translator=_FakeTranslator)
    monkeypatch.setattr("packages.engine_ct2.engine._load_ctranslate2", lambda: fake_ct2_module)

    engine = CTranslate2TranslatorEngine(model_path="/models/ct2-en-fr")
    request = _request(
        segments=(Segment(segment_id="s1", text="hello world\nthis is a plain text file"),)
    )

    result = engine.translate(request)
    assert result.translated_segments[0].text == "bonjour monde\nc ' est un fichier texte"
