from collections.abc import Sequence

import pytest

from packages.core.interfaces import DocumentAdapter, TranslatorEngine
from packages.core.models import DocumentFormat, Segment, TranslationRequest, TranslationResult


def test_abstract_interfaces_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        TranslatorEngine()  # type: ignore[abstract]
    with pytest.raises(TypeError):
        DocumentAdapter()  # type: ignore[abstract]


class _DummyTranslator(TranslatorEngine):
    def translate(self, request: TranslationRequest) -> TranslationResult:
        return TranslationResult(
            document_format=request.document_format,
            source_language=request.source_language,
            target_language=request.target_language,
            translated_segments=request.segments,
        )


class _DummyAdapter(DocumentAdapter):
    @property
    def supported_format(self) -> DocumentFormat:
        return DocumentFormat.TXT

    def extract_segments(self, document_bytes: bytes) -> tuple[Segment, ...]:
        return (Segment(segment_id="s1", text=document_bytes.decode("utf-8")),)

    def rebuild_document(
        self, original_document: bytes, translated_segments: Sequence[Segment]
    ) -> bytes:
        return "\n".join(segment.text for segment in translated_segments).encode("utf-8")


def test_dummy_implementations_satisfy_contracts() -> None:
    adapter = _DummyAdapter()
    segments = adapter.extract_segments(b"hello")
    request = TranslationRequest(
        document_format=DocumentFormat.TXT,
        source_language="en",
        target_language="fr",
        segments=segments,
    )
    translator = _DummyTranslator()
    result = translator.translate(request)

    assert adapter.supported_format is DocumentFormat.TXT
    assert result.translated_segments[0].text == "hello"
    assert adapter.rebuild_document(b"hello", result.translated_segments) == b"hello"
