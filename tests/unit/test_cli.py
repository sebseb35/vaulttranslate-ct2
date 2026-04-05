from pathlib import Path

from typer.testing import CliRunner

from apps.cli.main import app

runner = CliRunner()


def test_help_shows_translate_command() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "translate" in result.stdout


def test_translate_dry_run_outputs_summary(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.txt"
    output_path = tmp_path / "out.txt"
    input_path.write_text("hello", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "translate",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--source",
            "en",
            "--target",
            "fr",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    assert "Dry-run: no translation executed." in result.output
    assert "document_format=txt" in result.output
    assert f"input={input_path}" in result.output
    assert f"output={output_path}" in result.output


def test_translate_rejects_unsupported_extension(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.odt"
    output_path = tmp_path / "out.odt"
    input_path.write_text("hello", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "translate",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--source",
            "en",
            "--target",
            "fr",
            "--dry-run",
        ],
    )

    assert result.exit_code != 0
    assert "Unsupported input format" in result.output


def test_translate_rejects_missing_output_directory(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.txt"
    output_path = tmp_path / "missing" / "out.txt"
    input_path.write_text("hello", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "translate",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--source",
            "en",
            "--target",
            "fr",
            "--dry-run",
        ],
    )

    assert result.exit_code != 0
    assert "Output directory does not exist" in result.output


def test_translate_non_dry_run_reports_engine_not_wired(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.txt"
    output_path = tmp_path / "out.txt"
    input_path.write_text("hello", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "translate",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--source",
            "en",
            "--target",
            "fr",
        ],
    )

    assert result.exit_code == 0
    assert "Translation engine is not wired yet" in result.output