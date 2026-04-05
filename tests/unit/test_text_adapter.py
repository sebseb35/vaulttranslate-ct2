from pathlib import Path

import pytest

from packages.adapter_text import MarkdownDocumentAdapter, TxtDocumentAdapter
from packages.core.models import DocumentFormat, Segment


FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "text"


def _fixture_bytes(name: str) -> bytes:
    return (FIXTURES_DIR / name).read_bytes()


def test_txt_adapter_extract_and_rebuild_roundtrip() -> None:
    adapter = TxtDocumentAdapter()
    source = _fixture_bytes("plain_sample.txt")

    segments = adapter.extract_segments(source)

    assert adapter.supported_format is DocumentFormat.TXT
    assert len(segments) == 1
    assert segments[0].segment_id == "txt-0"
    assert segments[0].text == source.decode("utf-8")

    translated = (Segment(segment_id="txt-0", text="Bonjour monde.\nFichier texte.\n"),)
    rebuilt = adapter.rebuild_document(source, translated)
    assert rebuilt.decode("utf-8") == "Bonjour monde.\nFichier texte.\n"


def test_txt_adapter_rebuild_rejects_mismatched_segments() -> None:
    adapter = TxtDocumentAdapter()
    source = _fixture_bytes("plain_sample.txt")

    with pytest.raises(ValueError, match="exactly one segment"):
        adapter.rebuild_document(source, ())

    with pytest.raises(ValueError, match="txt-0"):
        adapter.rebuild_document(source, (Segment(segment_id="txt-1", text="x"),))

def test_txt_adapter_rejects_non_utf8_input() -> None:
    adapter = TxtDocumentAdapter()

    with pytest.raises(ValueError, match="UTF-8"):
        adapter.extract_segments(b"\xff\xfe\xfd")

def test_markdown_adapter_extract_preserves_code_fences() -> None:
    adapter = MarkdownDocumentAdapter()
    source = _fixture_bytes("markdown_sample.md")

    segments = adapter.extract_segments(source)
    text_blob = "\n".join(segment.text for segment in segments)

    assert adapter.supported_format is DocumentFormat.MD
    assert len(segments) == 3
    assert "def add(a, b):" not in text_blob
    assert "⟪VT_CODE_0⟫" in segments[1].text
    assert "⟪VT_LINK_URL_0⟫" in segments[1].text


def test_markdown_adapter_rebuild_restores_inline_code_and_links() -> None:
    adapter = MarkdownDocumentAdapter()
    source = _fixture_bytes("markdown_sample.md")
    extracted = adapter.extract_segments(source)

    translated = (
        Segment(segment_id=extracted[0].segment_id, text="# Bienvenue\n"),
        Segment(
            segment_id=extracted[1].segment_id,
            text=extracted[1].text.replace("Use", "Utilisez").replace("see", "consultez"),
        ),
        Segment(
            segment_id=extracted[2].segment_id,
            text=extracted[2].text.replace("Final line", "Ligne finale"),
        ),
    )

    rebuilt = adapter.rebuild_document(source, translated).decode("utf-8")

    assert "```python" in rebuilt
    assert "def add(a, b):" in rebuilt
    assert "`vaulttranslate run`" in rebuilt
    assert "`inline code`" in rebuilt
    assert "[Docs](https://example.com/docs)" in rebuilt
    assert "[Reference](https://example.org/ref)" in rebuilt
    assert "# Bienvenue" in rebuilt
    assert "Utilisez `vaulttranslate run` and consultez" in rebuilt
    assert "Ligne finale with [Reference](https://example.org/ref)" in rebuilt

def test_markdown_adapter_rebuild_rejects_segment_id_mismatch() -> None:
    adapter = MarkdownDocumentAdapter()
    source = _fixture_bytes("markdown_sample.md")
    extracted = adapter.extract_segments(source)

    translated = list(extracted)
    translated[0] = Segment(segment_id="wrong-id", text=translated[0].text)

    with pytest.raises(ValueError, match="segment mismatch"):
        adapter.rebuild_document(source, translated)
