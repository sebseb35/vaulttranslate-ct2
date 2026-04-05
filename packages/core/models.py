from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping


class DocumentFormat(StrEnum):
    DOCX = "docx"
    PPTX = "pptx"
    XLSX = "xlsx"
    PDF = "pdf"
    MD = "md"
    TXT = "txt"


@dataclass(frozen=True, slots=True)
class SegmentConstraints:
    max_chars: int | None = None
    preserve_whitespace: bool = True
    preserve_placeholders: bool = True

    def __post_init__(self) -> None:
        if self.max_chars is not None and self.max_chars <= 0:
            raise ValueError("max_chars must be greater than 0 when provided")


@dataclass(frozen=True, slots=True)
class Segment:
    segment_id: str
    text: str
    constraints: SegmentConstraints = field(default_factory=SegmentConstraints)

    def __post_init__(self) -> None:
        if not self.segment_id.strip():
            raise ValueError("segment_id must be a non-empty string")
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")


@dataclass(frozen=True, slots=True)
class TranslationRequest:
    document_format: DocumentFormat
    source_language: str
    target_language: str
    segments: tuple[Segment, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source_language.strip():
            raise ValueError("source_language must be a non-empty string")
        if not self.target_language.strip():
            raise ValueError("target_language must be a non-empty string")
        if not self.segments:
            raise ValueError("TranslationRequest requires at least one segment")


@dataclass(frozen=True, slots=True)
class TranslationResult:
    document_format: DocumentFormat
    source_language: str
    target_language: str
    translated_segments: tuple[Segment, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_language.strip():
            raise ValueError("source_language must be a non-empty string")
        if not self.target_language.strip():
            raise ValueError("target_language must be a non-empty string")
        if not self.translated_segments:
            raise ValueError("TranslationResult requires at least one translated segment")

