# Task

## Title
Implement CTranslate2 engine adapter

## Goal
Wrap local CTranslate2 usage behind the TranslatorEngine interface.

## Scope
- model path config
- batch translation of segments
- CPU threads config
- clean exceptions

## Constraints
- no model download logic
- no GPU assumptions
- keep it testable with mocks

## Deliverables
- engine_ct2 implementation
- unit tests
- optional slow integration test marker

## Validation
- pytest
- ruff check .
- mypy packages

## Out of scope
- model management UI
- benchmark suite

## Completion checklist
- [x] code added
- [x] tests added
- [x] validation passed
- [x] docs updated
- [x] issue closure comment posted
