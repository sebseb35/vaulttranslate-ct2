from __future__ import annotations

from pathlib import Path

import typer

from packages.core import DocumentFormat, Segment, TranslationRequest

app = typer.Typer(help="Offline document translation CLI.")

_SUFFIX_TO_FORMAT: dict[str, DocumentFormat] = {
    ".docx": DocumentFormat.DOCX,
    ".pptx": DocumentFormat.PPTX,
    ".xlsx": DocumentFormat.XLSX,
    ".pdf": DocumentFormat.PDF,
    ".md": DocumentFormat.MD,
    ".txt": DocumentFormat.TXT,
}

@app.callback()
def cli() -> None:
    """VaultTranslate command group."""


def infer_document_format(path: Path) -> DocumentFormat:
    document_format = _SUFFIX_TO_FORMAT.get(path.suffix.lower())
    if document_format is None:
        supported = ", ".join(fmt.value for fmt in DocumentFormat)
        raise typer.BadParameter(
            f"Unsupported input format for '{path.name}'. Supported formats: {supported}"
        )
    return document_format


@app.command()
def translate(
    input_path: Path = typer.Option(
        ...,
        "--input",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Path to the input document.",
    ),
    output_path: Path = typer.Option(
        ...,
        "--output",
        "-o",
        dir_okay=False,
        help="Path where translated output should be written.",
    ),
    source: str = typer.Option(..., "--source", "-s", help="Source language code (e.g. en)."),
    target: str = typer.Option(..., "--target", "-t", help="Target language code (e.g. fr)."),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Validate inputs and show a translation plan only."
    ),
) -> None:
    """Prepare a translation request skeleton."""
    document_format = infer_document_format(input_path)
    request = TranslationRequest(
        document_format=document_format,
        source_language=source,
        target_language=target,
        segments=(Segment(segment_id="segment-1", text=""),),
        metadata={
            "input_path": str(input_path),
            "output_path": str(output_path),
        },
    )
    if not output_path.parent.exists():
        raise typer.BadParameter(f"Output directory does not exist: {output_path.parent}")

    typer.echo("Prepared translation request:")
    typer.echo(f"document_format={request.document_format.value}")
    typer.echo(f"source={request.source_language}")
    typer.echo(f"target={request.target_language}")
    typer.echo(f"input={input_path}")
    typer.echo(f"output={output_path}")

    if dry_run:
        typer.echo("Dry-run: no translation executed.")
        raise typer.Exit(code=0)

    typer.echo("Translation engine is not wired yet. Re-run with --dry-run to preview request.")
    raise typer.Exit(code=0)

def main() -> None:
    """Console script entrypoint."""
    app()