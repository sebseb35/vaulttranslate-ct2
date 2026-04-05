from pathlib import Path

import pytest
from docx import Document

from packages.adapter_docx import DocxDocumentAdapter
from packages.core.models import DocumentFormat, Segment


FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "docx"


def _fixture_bytes(name: str) -> bytes:
    return (FIXTURES_DIR / name).read_bytes()


def test_docx_adapter_extracts_paragraphs_runs_tables_header_footer() -> None:
    adapter = DocxDocumentAdapter()
    source = _fixture_bytes("sample.docx")

    segments = adapter.extract_segments(source)
    texts = [segment.text for segment in segments]

    assert adapter.supported_format is DocumentFormat.DOCX
    assert all(segment.segment_id.startswith("docx-") for segment in segments)
    assert "Header text" in texts
    assert "Hello " in texts
    assert "world" in texts
    assert "Second paragraph" in texts
    assert "Cell A1" in texts
    assert "Cell B2" in texts
    assert "Footer text" in texts


def test_docx_adapter_rebuild_roundtrip_preserves_structure_and_updates_text(tmp_path: Path) -> None:
    adapter = DocxDocumentAdapter()
    source = _fixture_bytes("sample.docx")
    extracted = adapter.extract_segments(source)

    translated = tuple(
        Segment(segment_id=segment.segment_id, text=f"{segment.text} FR")
        for segment in extracted
    )
    rebuilt_bytes = adapter.rebuild_document(source, translated)

    output_path = tmp_path / "rebuilt.docx"
    output_path.write_bytes(rebuilt_bytes)
    doc = Document(output_path)

    assert doc.paragraphs[0].runs[0].text == "Hello  FR"
    assert doc.paragraphs[0].runs[1].text == "world FR"
    assert doc.paragraphs[0].runs[1].bold is True
    assert doc.paragraphs[1].text == "Second paragraph FR"
    assert doc.tables[0].cell(0, 0).text == "Cell A1 FR"
    assert doc.tables[0].cell(1, 1).text == "Cell B2 FR"
    assert doc.sections[0].header.paragraphs[0].text == "Header text FR"
    assert doc.sections[0].footer.paragraphs[0].text == "Footer text FR"


def test_docx_adapter_rebuild_validates_segment_count_and_ids() -> None:
    adapter = DocxDocumentAdapter()
    source = _fixture_bytes("sample.docx")
    extracted = adapter.extract_segments(source)

    with pytest.raises(ValueError, match="same number of segments"):
        adapter.rebuild_document(source, extracted[:-1])

    wrong_first = (Segment(segment_id="docx-9999", text="bad"),) + extracted[1:]
    with pytest.raises(ValueError, match="segment mismatch"):
        adapter.rebuild_document(source, wrong_first)

