import pytest

from packages.core.models import (
    DocumentFormat,
    Segment,
    SegmentConstraints,
    TranslationRequest,
    TranslationResult
)


def test_document_format_contains_expected_values() -> None:
    assert DocumentFormat.DOCX.value == "docx"
    assert DocumentFormat.PPTX.value == "pptx"
    assert DocumentFormat.XLSX.value == "xlsx"
    assert DocumentFormat.PDF.value == "pdf"
    assert DocumentFormat.MD.value == "md"
    assert DocumentFormat.TXT.value == "txt"


def test_segment_constraints_rejects_invalid_max_chars() -> None:
    with pytest.raises(ValueError, match="max_chars"):
        SegmentConstraints(max_chars=0)


def test_translation_result_requires_at_least_one_translated_segment() -> None:
    with pytest.raises(ValueError, match="at least one translated segment"):
        TranslationResult(
            document_format=DocumentFormat.TXT,
            source_language="en",
            target_language="fr",
            translated_segments=(),
        )


def test_translation_request_accepts_rich_metadata() -> None:
    segment = Segment(segment_id="s1", text="Hello")
    request = TranslationRequest(
        document_format=DocumentFormat.TXT,
        source_language="en",
        target_language="fr",
        segments=(segment,),
        metadata={"page": 1, "confidential": True},
    )
    assert request.metadata["page"] == 1
    assert request.metadata["confidential"] is True


def test_segment_requires_non_empty_segment_id() -> None:
    with pytest.raises(ValueError, match="segment_id"):
        Segment(segment_id="   ", text="Hello")


def test_segment_rejects_none_text() -> None:
    with pytest.raises(TypeError, match="text must be a string"):
        Segment(segment_id="s1", text=None)  # type: ignore[arg-type]