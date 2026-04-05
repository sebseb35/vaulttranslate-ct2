# Task

## Title
Implement DOCX adapter

## Goal
Extract and reinject translatable DOCX text while preserving structure.

## Scope
- paragraphs
- runs
- tables
- headers and footers

## Constraints
- use python-docx only
- do not support comments or tracked changes yet
- minimize formatting regressions
- add fixtures and tests

## Deliverables
- adapter_docx implementation
- fixtures
- unit tests

## Validation
- pytest
- ruff check .
- mypy packages

## Out of scope
- comments
- tracked changes
- smart art

## Completion checklist
- [x] code added
- [x] tests added
- [x] validation passed
- [x] docs updated
- [x] issue closure comment posted
