from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from .models import DocumentFormat, Segment, TranslationRequest, TranslationResult


class TranslatorEngine(ABC):
    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResult:
        """Translate request segments and return translated results."""


class DocumentAdapter(ABC):
    @property
    @abstractmethod
    def supported_format(self) -> DocumentFormat:
        """Return the document format handled by this adapter."""

    @abstractmethod
    def extract_segments(self, document_bytes: bytes) -> tuple[Segment, ...]:
        """Extract text segments from source document bytes."""

    @abstractmethod
    def rebuild_document(
        self, original_document: bytes, translated_segments: Sequence[Segment]
    ) -> bytes:
        """
        Rebuild document bytes with translated segments reinjected.
        translated_segments must correspond 1:1 with extract_segments output and preserve order and segment_id.
        """

