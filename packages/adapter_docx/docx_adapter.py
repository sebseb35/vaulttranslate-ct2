from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from io import BytesIO
from typing import Any

from docx import Document
from docx.document import Document as DocxDocument
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.section import _Footer, _Header
from docx.table import _Cell, Table
from docx.text.hyperlink import Hyperlink
from docx.text.paragraph import Paragraph
from docx.text.run import Run

from packages.core.interfaces import DocumentAdapter
from packages.core.models import DocumentFormat, Segment


@dataclass(frozen=True, slots=True)
class _TextTarget:
    kind: str
    node: Any
    original_texts: tuple[str, ...] = ()


class DocxDocumentAdapter(DocumentAdapter):
    @property
    def supported_format(self) -> DocumentFormat:
        return DocumentFormat.DOCX

    def extract_segments(self, document_bytes: bytes) -> tuple[Segment, ...]:
        doc = _load_document(document_bytes)
        targets = _collect_text_targets(doc)
        return tuple(
            Segment(
                segment_id=f"docx-{index}",
                text=_target_text(target),
            )
            for index, target in enumerate(targets)
        )

    def rebuild_document(
        self, original_document: bytes, translated_segments: Sequence[Segment]
    ) -> bytes:
        doc = _load_document(original_document)
        targets = _collect_text_targets(doc)

        if len(translated_segments) != len(targets):
            raise ValueError("DOCX rebuild requires the same number of segments as extraction")

        for idx, (target, translated_segment) in enumerate(
            zip(targets, translated_segments, strict=True)
        ):
            expected_id = f"docx-{idx}"
            if translated_segment.segment_id != expected_id:
                raise ValueError(
                    "DOCX segment mismatch: "
                    f"expected '{expected_id}' but got '{translated_segment.segment_id}'"
                )
            _set_target_text(target, translated_segment.text)

        output = BytesIO()
        doc.save(output)
        return output.getvalue()


def _load_document(document_bytes: bytes) -> DocxDocument:
    try:
        return Document(BytesIO(document_bytes))
    except Exception as exc:  # pragma: no cover - defensive handling
        raise ValueError("Failed to parse DOCX document bytes") from exc


def _collect_text_targets(doc: DocxDocument) -> list[_TextTarget]:
    targets: list[_TextTarget] = []

    for block in _iter_block_items(doc):
        _collect_block_text_targets(block, targets)

    for section in doc.sections:
        for block in _iter_block_items(section.header):
            _collect_block_text_targets(block, targets)
        for block in _iter_block_items(section.footer):
            _collect_block_text_targets(block, targets)

    return targets


def _collect_block_text_targets(block: Paragraph | Table, targets: list[_TextTarget]) -> None:
    if isinstance(block, Paragraph):
        inline_target = _paragraph_inline_target(block)
        if inline_target is not None:
            targets.append(inline_target)
            return

        if block.text != "":
            targets.append(_TextTarget(kind="paragraph", node=block))
        return

    if isinstance(block, Table):
        for row in block.rows:
            for cell in row.cells:
                for cell_block in _iter_block_items(cell):
                    _collect_block_text_targets(cell_block, targets)
        return

    raise TypeError(f"Unsupported block type: {type(block)!r}")


def _paragraph_inline_target(paragraph: Paragraph) -> _TextTarget | None:
    runs: list[Run] = []
    original_texts: list[str] = []

    for item in paragraph.iter_inner_content():
        if isinstance(item, Run):
            if item.text != "":
                runs.append(item)
                original_texts.append(item.text)
            continue

        if isinstance(item, Hyperlink):
            for run in item.runs:
                if run.text != "":
                    runs.append(run)
                    original_texts.append(run.text)
            continue

        raise TypeError(f"Unsupported paragraph content type: {type(item)!r}")

    if not runs:
        return None
    if len(runs) == 1:
        return _TextTarget(kind="run", node=runs[0], original_texts=(original_texts[0],))
    return _TextTarget(kind="inline-group", node=tuple(runs), original_texts=tuple(original_texts))


def _iter_block_items(parent: Any) -> Iterator[Paragraph | Table]:
    if isinstance(parent, DocxDocument):
        parent_element = parent.element.body
    elif isinstance(parent, _Cell):
        parent_element = parent._tc
    elif isinstance(parent, (_Header, _Footer)):
        parent_element = parent._element
    else:
        raise TypeError(f"Unsupported parent type: {type(parent)!r}")

    for child in parent_element.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def _target_text(target: _TextTarget) -> str:
    if target.kind == "run":
        value = getattr(target.node, "text", None)
        if not isinstance(value, str):
            raise TypeError("Run target text must be a string")
        return value
    if target.kind == "inline-group":
        return "".join(target.original_texts)
    if target.kind == "paragraph":
        value = getattr(target.node, "text", None)
        if not isinstance(value, str):
            raise TypeError("Paragraph target text must be a string")
        return value
    raise ValueError(f"Unsupported target kind: {target.kind}")


def _set_target_text(target: _TextTarget, text: str) -> None:
    if target.kind == "run":
        target.node.text = text
        return
    if target.kind == "inline-group":
        runs = target.node
        if not isinstance(runs, tuple):
            raise TypeError("Inline-group target must contain a tuple of runs")
        parts = _split_translated_text_across_runs(text, target.original_texts)
        for run, part in zip(runs, parts, strict=True):
            run.text = part
        return
    if target.kind == "paragraph":
        target.node.text = text
        return
    raise ValueError(f"Unsupported target kind: {target.kind}")


def _split_translated_text_across_runs(text: str, original_texts: tuple[str, ...]) -> tuple[str, ...]:
    if len(original_texts) == 1:
        return (text,)
    if text == "":
        return tuple("" for _ in original_texts)

    splits: list[int] = []
    total_original_length = sum(len(part) for part in original_texts)
    cumulative_length = 0

    for index, original_text in enumerate(original_texts[:-1]):
        cumulative_length += len(original_text)
        remaining_original = sum(len(part) for part in original_texts[index + 1 :])
        ideal_split = round(len(text) * cumulative_length / total_original_length)
        split_index = _adjust_split_index(
            text=text,
            ideal_split=ideal_split,
            current_text=original_text,
            next_text=original_texts[index + 1],
            min_index=(splits[-1] + 1) if splits else 1,
            max_index=len(text) - remaining_original,
        )
        splits.append(split_index)

    parts: list[str] = []
    start = 0
    for split_index in splits:
        parts.append(text[start:split_index])
        start = split_index
    parts.append(text[start:])
    return tuple(parts)


def _adjust_split_index(
    *,
    text: str,
    ideal_split: int,
    current_text: str,
    next_text: str,
    min_index: int,
    max_index: int,
) -> int:
    min_index = max(1, min_index)
    max_index = min(len(text) - 1, max_index)
    if min_index > max_index:
        return min_index

    whitespace_splits = [
        index
        for index in range(min_index, max_index + 1)
        if text[index - 1].isspace() or text[index].isspace()
    ]

    preferred: list[int] = []
    if current_text[-1:].isspace():
        preferred.extend(index for index in whitespace_splits if text[index - 1].isspace())
    if next_text[:1].isspace():
        preferred.extend(index for index in whitespace_splits if text[index].isspace())

    candidate_pool = preferred or whitespace_splits
    if candidate_pool:
        return min(candidate_pool, key=lambda idx: (abs(idx - ideal_split), idx))

    return min(max(ideal_split, min_index), max_index)
