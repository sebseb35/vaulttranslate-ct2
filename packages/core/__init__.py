"""Core domain contracts for translation workflows."""

from .interfaces import DocumentAdapter, TranslatorEngine
from .mock_engine import MockTranslatorEngine
from .models import (
    DocumentFormat,
    Segment,
    SegmentConstraints,
    TranslationRequest,
    TranslationResult,
)
from .pipeline import PipelineArtifacts, run_pipeline, select_adapter

__all__ = [
    "DocumentAdapter",
    "DocumentFormat",
    "MockTranslatorEngine",
    "PipelineArtifacts",
    "Segment",
    "SegmentConstraints",
    "TranslationRequest",
    "TranslationResult",
    "TranslatorEngine",
    "run_pipeline",
    "select_adapter",
]
