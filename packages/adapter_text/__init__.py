"""Text document adapters (TXT and Markdown)."""

from .markdown_adapter import MarkdownDocumentAdapter
from .txt_adapter import TxtDocumentAdapter

__all__ = ["MarkdownDocumentAdapter", "TxtDocumentAdapter"]
