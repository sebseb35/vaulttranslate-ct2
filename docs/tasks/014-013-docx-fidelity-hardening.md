# Task

## Metadata
- Issue: #14
- Status: done
- Priority: P2
- Type: feature
- Area: core

## Title
DOCX fidelity hardening

## Goal
Improve DOCX rebuild fidelity for richer inline content and additional real-world paragraph structures without sacrificing rebuild safety.

## Context
Imported from issue #14.

## Scope
- harden extraction and rebuild for mixed inline paragraph content such as hyperlinks
- validate behavior on a more realistic DOCX fixture

## Constraints
- Follow AGENTS.md and .codex/config.toml
- No new dependency unless justified
- Add or update tests

## Deliverables
- DOCX adapter hardening for mixed inline content
- additional DOCX fidelity tests and fixture coverage
- task metadata update

## Validation
- pytest -q
- ruff check .
- mypy packages

## Out of scope
- tracked changes support
- comments, SmartArt, or text boxes beyond trivial existing behavior

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
- [x] code added
- [x] tests added
- [x] validation passed
- [x] docs updated
- [x] issue closure comment posted
