from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TypeAlias
from collections.abc import Sequence

from packages.core import DocumentAdapter, DocumentFormat, Segment

_INLINE_CODE_PATTERN = re.compile(r"`[^`\n]*`")
_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)\n]+)\)")


@dataclass(frozen=True, slots=True)
class _LiteralBlock:
    text: str


@dataclass(frozen=True, slots=True)
class _SegmentBlock:
    segment_id: str
    token_map: dict[str, str]


MarkdownBlock: TypeAlias = _LiteralBlock | _SegmentBlock


@dataclass(frozen=True, slots=True)
class _MarkdownLayout:
    blocks: tuple[MarkdownBlock, ...]
    segments: tuple[Segment, ...]


class MarkdownDocumentAdapter(DocumentAdapter):
    @property
    def supported_format(self) -> DocumentFormat:
        return DocumentFormat.MD

    def extract_segments(self, document_bytes: bytes) -> tuple[Segment, ...]:
        markdown_text = _decode_utf8(document_bytes)
        layout = _build_markdown_layout(markdown_text)
        return layout.segments

    def rebuild_document(
        self, original_document: bytes, translated_segments: Sequence[Segment]
    ) -> bytes:
        markdown_text = _decode_utf8(original_document)
        layout = _build_markdown_layout(markdown_text)
        expected_ids = tuple(segment.segment_id for segment in layout.segments)

        if len(translated_segments) != len(expected_ids):
            raise ValueError("Markdown adapter rebuild requires the same number of segments")

        translated_by_id: dict[str, str] = {}
        for idx, translated in enumerate(translated_segments):
            expected_id = expected_ids[idx]
            if translated.segment_id != expected_id:
                raise ValueError(
                    f"Markdown segment mismatch at index {idx}: expected '{expected_id}', "
                    f"got '{translated.segment_id}'"
                )
            translated_by_id[translated.segment_id] = translated.text

        rebuilt_parts: list[str] = []
        for block in layout.blocks:
            if isinstance(block, _LiteralBlock):
                rebuilt_parts.append(block.text)
                continue
            translated_text = translated_by_id[block.segment_id]
            rebuilt_parts.append(_restore_placeholders(translated_text, block.token_map))

        return "".join(rebuilt_parts).encode("utf-8")


def _decode_utf8(document_bytes: bytes) -> str:
    try:
        return document_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Markdown adapter expects UTF-8 encoded input") from exc


def _build_markdown_layout(markdown_text: str) -> _MarkdownLayout:
    blocks: list[MarkdownBlock] = []
    segments: list[Segment] = []
    paragraph_buffer: list[str] = []
    segment_index = 0
    in_fenced_block = False
    fence_marker = ""

    def flush_paragraph() -> None:
        nonlocal segment_index
        if not paragraph_buffer:
            return

        paragraph_text = "".join(paragraph_buffer)
        paragraph_buffer.clear()

        masked_text, token_map = _mask_translatable_tokens(paragraph_text)
        segment_id = f"md-{segment_index}"
        segment_index += 1

        segments.append(Segment(segment_id=segment_id, text=masked_text))
        blocks.append(_SegmentBlock(segment_id=segment_id, token_map=token_map))

    for line in markdown_text.splitlines(keepends=True):
        marker = _fence_marker(line)
        if marker is not None:
            flush_paragraph()
            if not in_fenced_block:
                in_fenced_block = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fenced_block = False
                fence_marker = ""
            blocks.append(_LiteralBlock(text=line))
            continue

        if in_fenced_block:
            blocks.append(_LiteralBlock(text=line))
            continue

        if line.strip() == "":
            flush_paragraph()
            blocks.append(_LiteralBlock(text=line))
            continue

        paragraph_buffer.append(line)

    flush_paragraph()

    return _MarkdownLayout(blocks=tuple(blocks), segments=tuple(segments))


def _fence_marker(line: str) -> str | None:
    stripped = line.lstrip()
    if stripped.startswith("```"):
        return "```"
    if stripped.startswith("~~~"):
        return "~~~"
    return None


def _mask_translatable_tokens(paragraph_text: str) -> tuple[str, dict[str, str]]:
    token_map: dict[str, str] = {}
    code_index = 0

    def replace_inline_code(match: re.Match[str]) -> str:
        nonlocal code_index
        token = f"⟪VT_CODE_{code_index}⟫"
        token_map[token] = match.group(0)
        code_index += 1
        return token

    masked = _INLINE_CODE_PATTERN.sub(replace_inline_code, paragraph_text)

    link_index = 0

    def replace_link_url(match: re.Match[str]) -> str:
        nonlocal link_index
        label = match.group(1)
        url = match.group(2)
        token = f"⟪VT_LINK_URL_{link_index}⟫"
        token_map[token] = url
        link_index += 1
        return f"[{label}]({token})"

    masked = _LINK_PATTERN.sub(replace_link_url, masked)
    return masked, token_map


def _restore_placeholders(text: str, token_map: dict[str, str]) -> str:
    restored = text
    for token, original in token_map.items():
        restored = restored.replace(token, original)
    return restored
