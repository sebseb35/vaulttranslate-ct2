from io import BytesIO
from pathlib import Path

import pytest
from pypdf import PdfReader

from packages.core.models import DocumentFormat, Segment


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _build_text_pdf_bytes(pages: list[list[str]]) -> bytes:
    objects: list[bytes] = []

    def add_object(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    font_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids: list[int] = []

    for lines in pages:
        commands = ["BT", "/F1 12 Tf", "72 760 Td", "14 TL"]
        first = True
        for line in lines:
            escaped = _escape_pdf_text(line)
            if first:
                commands.append(f"({escaped}) Tj")
                first = False
            else:
                commands.append(f"T* ({escaped}) Tj")
        commands.append("ET")
        stream = "\n".join(commands).encode("utf-8")
        content_id = add_object(
            b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream"
        )
        page_id = add_object(
            (
                "<< /Type /Page /Parent PAGES_ID 0 R /MediaBox [0 0 612 792] "
                f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>"
            )
            .encode("ascii")
        )
        page_ids.append(page_id)

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    pages_body = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")
    pages_id = add_object(pages_body)

    for page_id in page_ids:
        page_body = objects[page_id - 1].replace(b"PAGES_ID", str(pages_id).encode("ascii"))
        objects[page_id - 1] = page_body

    catalog_id = add_object(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("ascii"))

    chunks = [b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"]
    offsets = [0]
    for index, body in enumerate(objects, start=1):
        offsets.append(sum(len(chunk) for chunk in chunks))
        chunks.append(f"{index} 0 obj\n".encode("ascii"))
        chunks.append(body)
        chunks.append(b"\nendobj\n")

    xref_offset = sum(len(chunk) for chunk in chunks)
    chunks.append(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    chunks.append(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        chunks.append(f"{offset:010d} 00000 n \n".encode("ascii"))
    chunks.append(
        (
            "trailer\n"
            f"<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
            "startxref\n"
            f"{xref_offset}\n"
            "%%EOF"
        ).encode("ascii")
    )
    return b"".join(chunks)


FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "pdf"


def _fixture_bytes(name: str) -> bytes:
    return (FIXTURES_DIR / name).read_bytes()


def test_pdf_adapter_extracts_text_paragraph_segments() -> None:
    from packages.adapter_pdf import PdfDocumentAdapter

    adapter = PdfDocumentAdapter()
    source = _fixture_bytes("sample.pdf")
    segments = adapter.extract_segments(source)

    assert adapter.supported_format is DocumentFormat.PDF
    assert segments == (
        Segment(segment_id="pdf-0", text="Quarterly report"),
        Segment(segment_id="pdf-1", text="Revenue up 12%"),
        Segment(segment_id="pdf-2", text="Margin stable"),
        Segment(segment_id="pdf-3", text="Second page intro"),
        Segment(segment_id="pdf-4", text="Follow-up note"),
    )


def test_pdf_adapter_rebuild_produces_readable_text_first_pdf() -> None:
    from packages.adapter_pdf import PdfDocumentAdapter

    source = _fixture_bytes("sample.pdf")
    adapter = PdfDocumentAdapter()
    extracted = adapter.extract_segments(source)
    translated = tuple(
        Segment(segment_id=segment.segment_id, text=f"{segment.text} FR")
        for segment in extracted
    )

    rebuilt_bytes = adapter.rebuild_document(source, translated)
    reader = PdfReader(BytesIO(rebuilt_bytes))
    extracted_pages = [page.extract_text() or "" for page in reader.pages]

    assert len(reader.pages) == 1
    assert "Quarterly report FR" in extracted_pages[0]
    assert "Revenue up 12% FR" in extracted_pages[0]
    assert "Margin stable FR" in extracted_pages[0]
    assert "Second page intro FR" in extracted_pages[0]
    assert "Follow-up note FR" in extracted_pages[0]


def test_pdf_adapter_rebuild_validates_segment_count_and_ids() -> None:
    from packages.adapter_pdf import PdfDocumentAdapter

    source = _build_text_pdf_bytes([["Alpha", "Beta"]])
    adapter = PdfDocumentAdapter()
    extracted = adapter.extract_segments(source)

    with pytest.raises(ValueError, match="same number of segments"):
        adapter.rebuild_document(source, extracted[:-1])

    wrong_first = (Segment(segment_id="pdf-9999", text="bad"),) + extracted[1:]
    with pytest.raises(ValueError, match="segment mismatch"):
        adapter.rebuild_document(source, wrong_first)
