# Task: Integration tests and packaging

## Goal
Stabilize MVP and make project runnable end-to-end.

## Requirements
- CLI end-to-end tests for:
  - txt
  - md
  - docx
- verify output files are written correctly

## Constraints
- no heavy dependencies
- deterministic tests

## Deliverables
- end-to-end CLI tests for txt, md, docx
- packaging improvements if needed (pyproject, install, entrypoint)
- README quickstart improvements
- minimal environment validation (clear errors if missing model/tokenizer)
- README quickstart

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
