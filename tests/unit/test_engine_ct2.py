from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

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


def test_engine_initializes_ctranslate2_translator_with_cpu_threads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    capture = _CallCapture()

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
            return [_FakeTranslationResult(["bonjour"])]

    fake_ct2_module = SimpleNamespace(Translator=_FakeTranslator)
    monkeypatch.setattr(
        "packages.engine_ct2.engine._load_ctranslate2",
        lambda: fake_ct2_module,
    )

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
    assert capture.batch_source == [["hello"]]
    assert result.translated_segments == (Segment(segment_id="s1", text="bonjour"),)


def test_engine_translates_segment_batch_preserving_order_and_ids(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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
            assert source == [["hello", "world"], ["how", "are", "you"]]
            return [
                _FakeTranslationResult(["bonjour", "monde"]),
                _FakeTranslationResult(["comment", "ca", "va"]),
            ]

    fake_ct2_module = SimpleNamespace(Translator=_FakeTranslator)
    monkeypatch.setattr(
        "packages.engine_ct2.engine._load_ctranslate2",
        lambda: fake_ct2_module,
    )

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
    monkeypatch.setattr(
        "packages.engine_ct2.engine._load_ctranslate2",
        lambda: fake_ct2_module,
    )

    engine = CTranslate2TranslatorEngine(model_path="/models/ct2-en-fr")

    with pytest.raises(CTranslate2EngineError, match="translation backend failed"):
        engine.translate(_request(segments=(Segment(segment_id="s1", text="hello"),)))

def test_engine_wraps_initialization_errors(monkeypatch: pytest.MonkeyPatch) -> None:
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
    monkeypatch.setattr(
        "packages.engine_ct2.engine._load_ctranslate2",
        lambda: fake_ct2_module,
    )

    with pytest.raises(CTranslate2EngineError, match="init backend failed"):
        CTranslate2TranslatorEngine(model_path="/models/ct2-en-fr")

def test_engine_rejects_result_count_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
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
            return [_FakeTranslationResult(["bonjour"])]

    fake_ct2_module = SimpleNamespace(Translator=_FakeTranslator)
    monkeypatch.setattr(
        "packages.engine_ct2.engine._load_ctranslate2",
        lambda: fake_ct2_module,
    )

    engine = CTranslate2TranslatorEngine(model_path="/models/ct2-en-fr")
    request = _request(
        segments=(
            Segment(segment_id="s1", text="hello"),
            Segment(segment_id="s2", text="world"),
        )
    )

    with pytest.raises(
        CTranslate2EngineError,
        match="different number of results",
    ):
        engine.translate(request)