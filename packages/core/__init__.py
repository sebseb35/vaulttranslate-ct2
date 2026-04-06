"""Core domain contracts for translation workflows."""

from typing import Any

from .interfaces import DocumentAdapter, TranslatorEngine
from .mock_engine import MockTranslatorEngine
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


def __getattr__(name: str) -> Any:
    if name in {"PipelineArtifacts", "run_pipeline", "select_adapter"}:
        from .pipeline import PipelineArtifacts, run_pipeline, select_adapter

        values = {
            "PipelineArtifacts": PipelineArtifacts,
            "run_pipeline": run_pipeline,
            "select_adapter": select_adapter,
        }
        return values[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
