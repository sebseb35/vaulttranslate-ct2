from __future__ import annotations

from collections.abc import Sequence
from io import BytesIO

from pypdf import PdfReader

from packages.core import DocumentAdapter, DocumentFormat, Segment


class PdfDocumentAdapter(DocumentAdapter):
    @property
    def supported_format(self) -> DocumentFormat:
        return DocumentFormat.PDF

    def extract_segments(self, document_bytes: bytes) -> tuple[Segment, ...]:
        reader = _load_pdf(document_bytes)
        lines = _extract_text_lines(reader)
        if not lines:
            raise ValueError("PDF adapter found no extractable text. OCR is not supported.")
        return tuple(
            Segment(segment_id=f"pdf-{index}", text=line)
            for index, line in enumerate(lines)
        )

    def rebuild_document(
        self, original_document: bytes, translated_segments: Sequence[Segment]
    ) -> bytes:
        original_segments = self.extract_segments(original_document)

        if len(translated_segments) != len(original_segments):
            raise ValueError("PDF rebuild requires the same number of segments as extraction")

        for index, translated in enumerate(translated_segments):
            expected_id = original_segments[index].segment_id
            if translated.segment_id != expected_id:
                raise ValueError(
                    "PDF segment mismatch: "
                    f"expected '{expected_id}' but got '{translated.segment_id}'"
                )

        return _build_simple_text_pdf([segment.text for segment in translated_segments])


def _load_pdf(document_bytes: bytes) -> PdfReader:
    try:
        return PdfReader(BytesIO(document_bytes))
    except Exception as exc:  # pragma: no cover - defensive handling
        raise ValueError("Failed to parse PDF document bytes") from exc


def _extract_text_lines(reader: PdfReader) -> list[str]:
    lines: list[str] = []
    for page in reader.pages:
        extracted = page.extract_text() or ""
        for raw_line in extracted.splitlines():
            line = raw_line.strip()
            if line != "":
                lines.append(line)
    return lines


def _build_simple_text_pdf(lines: Sequence[str], *, lines_per_page: int = 48) -> bytes:
    pages = [list(lines[index : index + lines_per_page]) for index in range(0, len(lines), lines_per_page)]
    objects: list[bytes] = []

    def add_object(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    font_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids: list[int] = []

    for page_lines in pages:
        commands = ["BT", "/F1 12 Tf", "72 760 Td", "14 TL"]
        first = True
        for line in page_lines:
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
            ).encode("ascii")
        )
        page_ids.append(page_id)

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    pages_id = add_object(
        f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")
    )

    for page_id in page_ids:
        objects[page_id - 1] = objects[page_id - 1].replace(
            b"PAGES_ID", str(pages_id).encode("ascii")
        )

    catalog_id = add_object(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("ascii"))

    chunks = [b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"]
    offsets = [0]
    current_offset = len(chunks[0])
    for index, body in enumerate(objects, start=1):
        offsets.append(current_offset)
        prefix = f"{index} 0 obj\n".encode("ascii")
        suffix = b"\nendobj\n"
        chunks.extend([prefix, body, suffix])
        current_offset += len(prefix) + len(body) + len(suffix)

    xref_offset = current_offset
    xref_header = f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    chunks.append(xref_header)
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


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
