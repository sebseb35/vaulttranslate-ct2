from __future__ import annotations

import re

from .interfaces import TranslatorEngine
from .models import Segment, TranslationRequest, TranslationResult


class MockTranslatorEngine(TranslatorEngine):
    """Deterministic local engine used when no real model is configured."""

    def translate(self, request: TranslationRequest) -> TranslationResult:
        translated_segments = tuple(
            Segment(
                segment_id=segment.segment_id,
                text=_append_language_suffix(segment.text, request.target_language),
                constraints=segment.constraints,
            )
            for segment in request.segments
        )

        return TranslationResult(
            document_format=request.document_format,
            source_language=request.source_language,
            target_language=request.target_language,
            translated_segments=translated_segments,
            metadata={**request.metadata, "engine": "mock"},
        )


_TRAILING_WHITESPACE_PATTERN = re.compile(r"(\s*)$")


def _append_language_suffix(text: str, target_language: str) -> str:
    suffix = f" [{target_language}]"
    match = _TRAILING_WHITESPACE_PATTERN.search(text)
    if match is None:
        return text + suffix
    trailing = match.group(1)
    base = text[: len(text) - len(trailing)]
    return f"{base}{suffix}{trailing}"
