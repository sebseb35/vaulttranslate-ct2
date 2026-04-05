from __future__ import annotations

from pathlib import Path

from packages.engine_ct2 import CTranslate2TranslatorEngine

from .interfaces import TranslatorEngine
from .mock_engine import MockTranslatorEngine


def select_engine(
    *,
    model_path: Path | None,
    tokenizer_path: str | None = None,
    inter_threads: int = 1,
    intra_threads: int = 1,
    compute_type: str = "default",
) -> TranslatorEngine:
    if model_path is None:
        return MockTranslatorEngine()

    return CTranslate2TranslatorEngine(
        model_path=str(model_path),
        tokenizer_path=tokenizer_path,
        inter_threads=inter_threads,
        intra_threads=intra_threads,
        compute_type=compute_type,
    )
