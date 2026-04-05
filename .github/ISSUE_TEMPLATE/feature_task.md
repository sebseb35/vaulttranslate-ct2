---
name: Task
about: Backlog item to execute with Codex using a task contract
title: "[task] "
labels: ["status:ready", "type:feature", "priority:P2", "area:core"]
assignees: []
---

## Why
Describe user/developer impact.

## What
Describe expected outcome and acceptance criteria.

## Scope
- item
- item

## Constraints
- No cloud APIs
- CPU-only
- No OCR
- Keep architecture stable unless justified

## Deliverables
- code
- tests
- docs update if needed

## Validation
- pytest -q
- ruff check .
- mypy packages

## Task Contract
- [ ] Create/update `docs/tasks/NNN-MMM-slug.md`
