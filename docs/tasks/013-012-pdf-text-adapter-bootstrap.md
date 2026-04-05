# Task

## Metadata
- Issue: #13
- Status: done
- Priority: P2
- Type: feature
- Area: core

## Title
PDF text adapter bootstrap

## Goal
Add initial text-only PDF translation support that can extract readable text from text PDFs and rebuild translated output in a simple text-first PDF form.

## Context
Imported from issue #13.

## Scope
- extract text lines from text-based PDF pages
- rebuild translated output as a simple readable PDF

## Constraints
- Follow AGENTS.md and .codex/config.toml
- No new dependency unless justified
- Add or update tests

## Deliverables
- PDF adapter implementation
- unit tests for extraction, rebuild, pipeline, and CLI handling
- task metadata update

## Validation
- pytest -q
- ruff check .
- mypy packages

## Out of scope
- OCR or scanned PDFs
- pixel-perfect visual reconstruction

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
- [x] code added
- [x] tests added
- [x] validation passed
- [x] docs updated
- [x] issue closure comment posted
