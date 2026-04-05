# Task

## Title
Implement TXT and Markdown adapter

## Goal
Support extraction and reinjection for txt and md files.

## Scope
- plain text
- markdown paragraphs
- preserve fenced code blocks
- preserve inline code and links where possible

## Constraints
- no extra dependency unless justified
- keep implementation modular
- add fixtures and tests

## Deliverables
- adapter_text implementation
- test fixtures
- unit tests

## Validation
- pytest
- ruff check .
- mypy packages

## Out of scope
- HTML conversion
- advanced markdown AST rewriting

## Completion checklist
- [x] code added
- [x] tests added
- [x] validation passed
- [x] docs updated
- [x] issue closure comment posted
