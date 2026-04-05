# Task

## Metadata
- Issue: #13
- Status: ready
- Priority: P2
- Type: feature
- Area: core

## Title
PDF text adapter bootstrap

## Goal
Describe what should exist when this task is done.

## Context
Imported from issue #13.

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
Add initial PDF text-only translation support.

## Why
PDF is a common enterprise format, but should start with text PDFs only for a reliable MVP.

## Scope
- support text-based PDFs only
- extract text blocks/paragraphs
- rebuild output in a simple, usable form
- preserve content fidelity over visual fidelity

## Constraints
- no OCR
- no scanned PDFs
- no promise of pixel-perfect reconstruction
- keep implementation simple and explicit

## Acceptance criteria
- can extract text from a sample text-PDF
- can rebuild translated output in an acceptable text-first form
- tests pass

## Suggested task file
docs/tasks/012-pdf-text-adapter-bootstrap.md

## Completion checklist
- [ ] code added
- [ ] tests added
- [ ] validation passed
- [ ] docs updated
- [ ] issue closure comment posted
