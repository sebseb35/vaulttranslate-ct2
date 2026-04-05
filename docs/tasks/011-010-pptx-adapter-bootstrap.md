# Task

## Metadata
- Issue: #11
- Status: ready
- Priority: P2
- Type: feature
- Area: core

## Title
PPTX adapter bootstrap

## Goal
Describe what should exist when this task is done.

## Context
Imported from issue #11.

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
Add initial PPTX translation support for the local document translation pipeline.

## Why
PowerPoint is a high-value enterprise format and a natural next step after DOCX support.

## Scope
- extract translatable text from slides
- support text frames / shapes
- support table cell text
- rebuild translated PPTX while preserving structure as much as possible

## Constraints
- no OCR
- no comments/review features
- no heavy dependency beyond python-pptx if needed
- keep adapter logic decoupled from engine and CLI

## Acceptance criteria
- can extract segments from a sample PPTX
- can rebuild a translated PPTX
- segment IDs are stable and validated on rebuild
- tests pass

## Suggested task file
docs/tasks/010-pptx-adapter-bootstrap.md

## Completion checklist
- [x] code added
- [x] tests added
- [x] validation passed
- [x] docs updated
- [x] issue closure comment posted
