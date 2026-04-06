# Task

## Metadata
- Issue: #18
- Status: done
- Priority: P2
- Type: feature
- Area: core

## Title
DOCX semantic run grouping for safer translation

## Goal
Reduce DOCX mistranslations caused by run-level fragmentation by grouping compatible adjacent inline content into safer semantic translation units.

## Context
Imported from issue #18.

## Scope
- group compatible adjacent inline content within DOCX paragraphs into larger translation units
- preserve rebuild predictability while redistributing translated text back into the original runs

## Constraints
- Follow AGENTS.md and .codex/config.toml
- No new dependency unless justified
- Add or update tests

## Deliverables
- DOCX semantic run grouping implementation
- regression tests for semantic grouping and rebuild distribution
- task metadata update

## Validation
- pytest -q
- ruff check .
- mypy packages

## Out of scope
- tracked changes support
- comments or complex text-box handling

## Imported issue body
## Why
DOCX translation currently segments many paragraphs at run granularity to preserve formatting, but that can produce poor semantic translation when a sentence is split across styled runs. A concrete example is `Hello world` becoming `Bonjour.monde entier` because adjacent runs are translated independently and then reassembled.

## What
Harden DOCX translation semantics by grouping compatible adjacent inline content into larger translation units when doing so is safe, while preserving rebuild predictability and formatting as much as possible.

## Scope
- identify safe grouping rules for adjacent DOCX runs and hyperlinks within a paragraph
- avoid translating sentence fragments independently when they belong to the same phrase or sentence
- preserve hyperlink URLs and basic run formatting during rebuild
- add regression coverage for multi-run semantic translation cases

## Constraints
- No cloud APIs
- CPU-only
- No OCR
- Keep architecture stable unless justified
- no tracked changes support
- no comments support

## Deliverables
- code
- tests
- docs update if needed

## Validation
- pytest -q
- ruff check .
- mypy packages

## Completion checklist
- [x] code added
- [x] tests added
- [x] validation passed
- [x] docs updated
- [ ] issue closure comment posted
