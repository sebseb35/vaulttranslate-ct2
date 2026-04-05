# Task: End-to-end pipeline (TXT, MD, DOCX)

## Goal
Wire CLI, adapters and engine into a working translation pipeline.

## Scope
- Supported formats: txt, md, docx
- No OCR
- No cloud
- No automatic model download

## Requirements
- Select adapter from input file extension
- Extract segments from document
- Build TranslationRequest
- Call TranslatorEngine
- Rebuild translated document
- Write output file

## CLI behavior
- --dry-run: only print request summary
- normal mode: write translated file

## Constraints
- keep CLI thin
- keep adapters and engine decoupled
- no over-engineering

## Deliverables
- CLI integration code
- adapter selection logic
- output writing
- tests (unit or integration)
- updated README if needed

## Validation
- pytest -q
- ruff check .
- mypy packages

## Completion checklist
- [x] code added
- [x] tests added
- [x] validation passed
- [x] docs updated
- [x] issue closure comment posted
