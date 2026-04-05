# Task

## Metadata
- Issue: #12
- Status: ready
- Priority: P2
- Type: feature
- Area: core

## Title
XLSX adapter bootstrap

## Goal
Describe what should exist when this task is done.

## Context
Imported from issue #12.

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
Add initial XLSX translation support for the local document translation pipeline.

## Why
Excel is a core enterprise document format and required for practical MVP expansion.

## Scope
- extract translatable text cells from worksheets
- preserve workbook structure
- avoid modifying formulas
- rebuild translated XLSX while preserving sheet data integrity

## Constraints
- do not translate formulas
- no macros/VBA handling
- no charts or advanced objects in this first iteration
- keep adapter logic decoupled from engine and CLI

## Acceptance criteria
- can extract text segments from a sample XLSX
- formulas remain unchanged
- can rebuild a translated XLSX
- tests pass

## Suggested task file
docs/tasks/011-xlsx-adapter-bootstrap.md

## Completion checklist
- [ ] code added
- [ ] tests added
- [ ] validation passed
- [ ] docs updated
- [ ] issue closure comment posted
