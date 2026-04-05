# Task

## Metadata
- Issue: #14
- Status: ready
- Priority: P2
- Type: feature
- Area: core

## Title
DOCX fidelity hardening

## Goal
Describe what should exist when this task is done.

## Context
Imported from issue #14.

## Scope
- item
- item

## Constraints
- Follow AGENTS.md and .codex/config.toml
- No new dependency unless justified
- Add or update tests

## Deliverables
- implementation
- tests
- docs update if needed

## Validation
- pytest -q
- ruff check .
- mypy packages

## Out of scope
- item
- item

## Imported issue body
## Goal
Improve DOCX rebuild fidelity and edge-case handling.

## Why
DOCX support exists, but product quality depends on handling additional real-world document structures more robustly.

## Scope
- review extraction/rebuild edge cases
- improve paragraph/run fidelity where possible
- validate behavior on more realistic sample files
- keep rebuild safe and predictable

## Constraints
- no tracked changes support
- no comments support
- no SmartArt/text boxes in this iteration unless trivial
- avoid over-engineering

## Acceptance criteria
- improved behavior on additional DOCX fixtures
- no regressions on current DOCX tests
- tests pass

## Suggested task file
docs/tasks/013-docx-fidelity-hardening.md

## Completion checklist
- [ ] code added
- [ ] tests added
- [ ] validation passed
- [ ] docs updated
- [ ] issue closure comment posted
