# vaulttranslate-ct2
Private, on-device document translation for enterprise. Translate DOCX, PPTX, XLSX, PDF, MD, and TXT locally with structure-preserving adapters where practical. PDF support is intentionally text-first rather than visually faithful. No cloud, no data leakage, CPU-only.

## Quickstart
Install default local/mock mode:

```bash
pip install -e .
```

Install optional real CT2 mode:

```bash
pip install -e ".[ct2]"
```

Workflow docs:
- `docs/agentic-workflow.md`
- `docs/backlog-status.md`
- `docs/decisions/README.md`
- `docs/roadmap.md`

Run a dry-run request preview:

```bash
vaulttranslate translate \
  --input ./document.txt \
  --output ./document.fr.txt \
  --source en \
  --target fr \
  --dry-run
```

Run without `--dry-run` to execute the local pipeline (`txt`, `md`, `docx`, `pptx`, `xlsx`, `pdf`) and write output:

```bash
vaulttranslate translate \
  --input ./document.txt \
  --output ./document.fr.txt \
  --source en \
  --target fr
```

Optional real CTranslate2 mode (CPU-only) by passing a local model directory:

```bash
vaulttranslate translate \
  --input ./document.txt \
  --output ./document.fr.txt \
  --source en \
  --target fr \
  --model-path /path/to/ct2-model \
  --tokenizer-path /path/to/tokenizer-or-local-hf-cache \
  --inter-threads 2 \
  --intra-threads 4
```

For multiline TXT content, the CT2 path preserves newline structure and translates line chunks to avoid dropped content.
When using `--model-path`, the CLI validates that model/tokenizer directories exist and reports clear errors.

## Format Notes
- `txt`: round-trip text output
- `md`: preserves fenced code blocks and protects inline code and links where possible
- `docx`, `pptx`, `xlsx`: preserve document/workbook structure as much as possible
- `pdf`: text-only extraction and simple text-first PDF rebuild, with no OCR and no visual fidelity guarantee

## License
This project is licensed under Apache-2.0. Current declared dependencies are permissive-license compatible (`MIT`, `BSD-3-Clause`, `Apache-2.0`).

## Backlog Utilities
Local helper commands:

```bash
scripts/new-task.sh <issue_number> [slug]
scripts/run-task.sh docs/tasks/<task-file>.md
scripts/list-tasks.sh
scripts/list-pending-tasks.sh
scripts/summarize-completed-tasks.sh
scripts/snapshot-backlog.sh
```

Equivalent Makefile targets:

```bash
make tasks
make tasks-pending
make tasks-done
make tasks-snapshot
```

## Real CT2 Smoke Test (Optional)
No model is downloaded automatically. Place a compatible CTranslate2 model folder locally, then run:

```bash
export VT_CT2_MODEL_PATH=/path/to/ct2-model
./.venv/bin/pytest -q tests/integration/test_real_ct2_smoke.py
```

Manual CLI check (TXT):

```bash
vaulttranslate translate \
  --input ./sample.txt \
  --output ./sample.fr.txt \
  --source en \
  --target fr \
  --model-path "$VT_CT2_MODEL_PATH"
```

Manual CLI check (MD):

```bash
vaulttranslate translate \
  --input ./sample.md \
  --output ./sample.fr.md \
  --source en \
  --target fr \
  --model-path "$VT_CT2_MODEL_PATH"
```
