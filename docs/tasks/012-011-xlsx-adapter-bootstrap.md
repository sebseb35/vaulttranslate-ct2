# Task

## Metadata
- Issue: #12
- Status: done
- Priority: P2
- Type: feature
- Area: core

## Title
XLSX adapter bootstrap

## Goal
Add initial XLSX translation support that can extract text cells, preserve workbook structure, skip formulas, and rebuild translated workbooks safely.

## Context
Imported from issue #12.

## Scope
- extract translatable worksheet cell text
- rebuild translated XLSX content without changing formulas

## Constraints
- Follow AGENTS.md and .codex/config.toml
- No new dependency unless justified
- Add or update tests

## Deliverables
- XLSX adapter implementation
- unit tests and real XLSX fixtures
- task and backlog metadata update

## Validation
- pytest -q
- ruff check .
- mypy packages

## Out of scope
- macros / VBA handling
- charts, comments, and advanced workbook objects

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
- [x] code added
- [x] tests added
- [x] validation passed
- [x] docs updated
- [x] issue closure comment posted
