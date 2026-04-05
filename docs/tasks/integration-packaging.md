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
- integration tests
- packaging improvements
- README quickstart

## Validation
- pytest -q
- ruff check .
- mypy packages