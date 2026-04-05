import pytest

from packages.core import (
    DocumentFormat,
    MockTranslatorEngine,
    run_pipeline,
    select_adapter,
)


def test_select_adapter_supports_txt_md_docx() -> None:
    assert select_adapter(DocumentFormat.TXT).supported_format is DocumentFormat.TXT
    assert select_adapter(DocumentFormat.MD).supported_format is DocumentFormat.MD
    assert select_adapter(DocumentFormat.DOCX).supported_format is DocumentFormat.DOCX


def test_select_adapter_rejects_unsupported_format() -> None:
    with pytest.raises(ValueError, match="No adapter configured"):
        select_adapter(DocumentFormat.PDF)


def test_run_pipeline_translates_txt_document_bytes() -> None:
    adapter = select_adapter(DocumentFormat.TXT)
    engine = MockTranslatorEngine()

    artifacts = run_pipeline(
        document_bytes=b"hello world",
        adapter=adapter,
        source_language="en",
        target_language="fr",
        input_path="/tmp/in.txt",
        output_path="/tmp/out.txt",
        engine=engine,
    )

    assert artifacts.request.document_format is DocumentFormat.TXT
    assert artifacts.result.metadata["engine"] == "mock"
    assert artifacts.output_bytes.decode("utf-8") == "hello world [fr]"

