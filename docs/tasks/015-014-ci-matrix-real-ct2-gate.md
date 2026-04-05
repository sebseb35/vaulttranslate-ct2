# Task

## Metadata
- Issue: #15
- Status: ready
- Priority: P2
- Type: feature
- Area: core

## Title
CI matrix and optional real CT2 validation gate

## Goal
Describe what should exist when this task is done.

## Context
Imported from issue #15.

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
Improve CI quality gates while keeping real CT2 validation optional and local-friendly.

## Why
The project now has a real MVP and needs stronger automated validation without forcing heavy model-dependent checks on every run.

## Scope
- improve CI job structure
- keep default checks lightweight and deterministic
- add optional/manual real CT2 validation path
- document expected CI/dev workflow

## Constraints
- do not require local models in default CI
- keep real-model checks optional/manual
- avoid over-engineering

## Acceptance criteria
- CI clearly covers lint/type/tests
- optional real CT2 validation path is documented
- contributors can understand default vs optional validation paths

## Suggested task file
docs/tasks/014-ci-matrix-real-ct2-gate.md

## Completion checklist
- [ ] code added
- [ ] tests added
- [ ] validation passed
- [ ] docs updated
- [ ] issue closure comment posted
