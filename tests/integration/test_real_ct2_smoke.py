from __future__ import annotations

import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from apps.cli.main import app

runner = CliRunner()


@pytest.mark.skipif(
    "VT_CT2_MODEL_PATH" not in os.environ,
    reason="Set VT_CT2_MODEL_PATH to run real CTranslate2 smoke test",
)
def test_real_ct2_smoke_txt_and_md(tmp_path: Path) -> None:
    ctranslate2 = pytest.importorskip("ctranslate2")
    del ctranslate2

    model_path = Path(os.environ["VT_CT2_MODEL_PATH"])
    if not model_path.exists():
        pytest.skip(f"VT_CT2_MODEL_PATH does not exist: {model_path}")

    fixture_txt = Path(__file__).resolve().parents[1] / "fixtures" / "text" / "plain_sample.txt"
    txt_in = tmp_path / "sample.txt"
    txt_out = tmp_path / "sample.fr.txt"
    txt_in.write_text(fixture_txt.read_text(encoding="utf-8"), encoding="utf-8")

    txt_result = runner.invoke(
        app,
        [
            "translate",
            "--input",
            str(txt_in),
            "--output",
            str(txt_out),
            "--source",
            "en",
            "--target",
            "fr",
            "--model-path",
            str(model_path),
        ],
    )
    assert txt_result.exit_code == 0
    assert txt_out.exists()
    txt_content = txt_out.read_text(encoding="utf-8")
    assert txt_content != ""
    non_empty_lines = [line for line in txt_content.splitlines() if line.strip()]
    assert len(non_empty_lines) >= 2

    md_in = tmp_path / "sample.md"
    md_out = tmp_path / "sample.fr.md"
    md_in.write_text(
        "Hello markdown.\n\n```python\nprint('smoke')\n```\n",
        encoding="utf-8",
    )

    md_result = runner.invoke(
        app,
        [
            "translate",
            "--input",
            str(md_in),
            "--output",
            str(md_out),
            "--source",
            "en",
            "--target",
            "fr",
            "--model-path",
            str(model_path),
        ],
    )
    assert md_result.exit_code == 0
    assert md_out.exists()
    md_text = md_out.read_text(encoding="utf-8")
    assert md_text != ""
    assert "```python" in md_text
