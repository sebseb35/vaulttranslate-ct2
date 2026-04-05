"""Core domain contracts for translation workflows."""

from .interfaces import DocumentAdapter, TranslatorEngine
from .models import (
    DocumentFormat,
    Segment,
    SegmentConstraints,
    TranslationRequest,
    TranslationResult,
)

__all__ = [
    "DocumentAdapter",
    "DocumentFormat",
    "Segment",
    "SegmentConstraints",
    "TranslationRequest",
    "TranslationResult",
    "TranslatorEngine",
]

