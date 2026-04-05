from __future__ import annotations

from pathlib import Path

import typer

from packages.engine_ct2 import CTranslate2EngineError
from packages.core.models import DocumentFormat
from packages.core.pipeline import run_pipeline, select_adapter
from packages.core.engine_selection import select_engine

app = typer.Typer(help="Offline document translation CLI.")

_SUFFIX_TO_FORMAT: dict[str, DocumentFormat] = {
    ".docx": DocumentFormat.DOCX,
    ".md": DocumentFormat.MD,
    ".pdf": DocumentFormat.PDF,
    ".txt": DocumentFormat.TXT,
    ".pptx": DocumentFormat.PPTX,
    ".xlsx": DocumentFormat.XLSX,
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


def _validate_engine_paths(
    *,
    model_path: Path | None,
    tokenizer_path: str | None,
) -> None:
    if tokenizer_path is not None and model_path is None:
        raise typer.BadParameter("--tokenizer-path requires --model-path")

    if model_path is None:
        return

    if not model_path.exists():
        raise typer.BadParameter(f"Model path does not exist: {model_path}")
    if not model_path.is_dir():
        raise typer.BadParameter(f"Model path must be a directory: {model_path}")

    if tokenizer_path is None:
        return

    tokenizer_dir = Path(tokenizer_path).expanduser()
    if not tokenizer_dir.exists():
        raise typer.BadParameter(f"Tokenizer path does not exist: {tokenizer_path}")
    if not tokenizer_dir.is_dir():
        raise typer.BadParameter(f"Tokenizer path must be a directory: {tokenizer_path}")


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
    model_path: Path | None = typer.Option(
        None,
        "--model-path",
        help="Optional CTranslate2 model directory. Uses mock engine when omitted.",
    ),
    tokenizer_path: str | None = typer.Option(
        None,
        "--tokenizer-path",
        help="Optional tokenizer path/reference for CTranslate2 mode.",
    ),
    inter_threads: int = typer.Option(
        1,
        "--inter-threads",
        min=1,
        help="CPU inter-op threads for CTranslate2 (when model-path is set).",
    ),
    intra_threads: int = typer.Option(
        1,
        "--intra-threads",
        min=1,
        help="CPU intra-op threads for CTranslate2 (when model-path is set).",
    ),
    compute_type: str = typer.Option(
        "default",
        "--compute-type",
        help="CTranslate2 compute type, e.g. default/int8/float32.",
    ),
) -> None:
    """Translate a document end-to-end using local adapters and engine."""
    document_format = infer_document_format(input_path)
    if not output_path.parent.exists():
        raise typer.BadParameter(f"Output directory does not exist: {output_path.parent}")
    _validate_engine_paths(model_path=model_path, tokenizer_path=tokenizer_path)

    adapter = select_adapter(document_format)
    document_bytes = input_path.read_bytes()
    segments = adapter.extract_segments(document_bytes)
    engine_mode = "ctranslate2" if model_path is not None else "mock"

    typer.echo("Prepared translation request:")
    typer.echo(f"document_format={document_format.value}")
    typer.echo(f"source={source}")
    typer.echo(f"target={target}")
    typer.echo(f"input={input_path}")
    typer.echo(f"output={output_path}")
    typer.echo(f"segments={len(segments)}")
    typer.echo(f"engine={engine_mode}")
    if model_path is not None:
        typer.echo(f"model_path={model_path}")
        if tokenizer_path is not None:
            typer.echo(f"tokenizer_path={tokenizer_path}")

    if dry_run:
        typer.echo("Dry-run: no translation executed.")
        raise typer.Exit(code=0)

    try:
        engine = select_engine(
            model_path=model_path,
            tokenizer_path=tokenizer_path,
            inter_threads=inter_threads,
            intra_threads=intra_threads,
            compute_type=compute_type,
        )
        artifacts = run_pipeline(
            document_bytes=document_bytes,
            adapter=adapter,
            source_language=source,
            target_language=target,
            input_path=str(input_path),
            output_path=str(output_path),
            engine=engine,
        )
    except CTranslate2EngineError as exc:
        typer.secho(f"CTranslate2 error: {exc}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc

    output_path.write_bytes(artifacts.output_bytes)
    typer.echo(f"Wrote translated file to {output_path}")
    raise typer.Exit(code=0)

def main() -> None:
    """Console script entrypoint."""
    app()
