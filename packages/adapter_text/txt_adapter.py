from __future__ import annotations

from collections.abc import Sequence

from packages.core import DocumentAdapter, DocumentFormat, Segment


class TxtDocumentAdapter(DocumentAdapter):
    @property
    def supported_format(self) -> DocumentFormat:
        return DocumentFormat.TXT

    def extract_segments(self, document_bytes: bytes) -> tuple[Segment, ...]:
        try:
            text = document_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("TXT adapter expects UTF-8 encoded input") from exc
        return (Segment(segment_id="txt-0", text=text),)

    def rebuild_document(
        self, original_document: bytes, translated_segments: Sequence[Segment]
    ) -> bytes:
        del original_document
        if len(translated_segments) != 1:
            raise ValueError("TXT adapter rebuild requires exactly one segment")
        segment = translated_segments[0]
        if segment.segment_id != "txt-0":
            raise ValueError("TXT adapter expects translated segment_id to be 'txt-0'")
        return segment.text.encode("utf-8")
