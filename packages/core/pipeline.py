from __future__ import annotations

from dataclasses import dataclass

from packages.adapter_docx import DocxDocumentAdapter
from packages.adapter_text import MarkdownDocumentAdapter, TxtDocumentAdapter

from .interfaces import DocumentAdapter, TranslatorEngine
from .models import DocumentFormat, Segment, TranslationRequest, TranslationResult


@dataclass(frozen=True, slots=True)
class PipelineArtifacts:
    request: TranslationRequest
    result: TranslationResult
    output_bytes: bytes


def select_adapter(document_format: DocumentFormat) -> DocumentAdapter:
    if document_format is DocumentFormat.TXT:
        return TxtDocumentAdapter()
    if document_format is DocumentFormat.MD:
        return MarkdownDocumentAdapter()
    if document_format is DocumentFormat.DOCX:
        return DocxDocumentAdapter()
    raise ValueError(f"No adapter configured for document format '{document_format.value}'")


def build_request(
    *,
    document_format: DocumentFormat,
    source_language: str,
    target_language: str,
    segments: tuple[Segment, ...],
    input_path: str,
    output_path: str,
) -> TranslationRequest:
    return TranslationRequest(
        document_format=document_format,
        source_language=source_language,
        target_language=target_language,
        segments=segments,
        metadata={"input_path": input_path, "output_path": output_path},
    )


def run_pipeline(
    *,
    document_bytes: bytes,
    adapter: DocumentAdapter,
    source_language: str,
    target_language: str,
    input_path: str,
    output_path: str,
    engine: TranslatorEngine,
) -> PipelineArtifacts:
    segments = adapter.extract_segments(document_bytes)
    request = build_request(
        document_format=adapter.supported_format,
        source_language=source_language,
        target_language=target_language,
        segments=segments,
        input_path=input_path,
        output_path=output_path,
    )
    result = engine.translate(request)
    output_bytes = adapter.rebuild_document(document_bytes, result.translated_segments)
    return PipelineArtifacts(request=request, result=result, output_bytes=output_bytes)
