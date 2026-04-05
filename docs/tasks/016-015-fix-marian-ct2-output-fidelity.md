# Task

## Metadata
- Issue: #16
- Status: done
- Priority: P1
- Type: tech-debt
- Area: engine

## Title
Fix Marian CT2 output fidelity

## Goal
Ensure real CLI translation with Marian/OPUS-MT preserves the full source content and produces complete output.

## Context
The CLI could run real local CT2 translation with a Marian model and local tokenizer, but output fidelity was incorrect on a simple TXT fixture:
- source: two sentences
- output: only one translated sentence

## Scope
- investigate tokenizer and decoding behavior for Marian/OPUS-MT
- compare current engine behavior with the standalone smoke test
- ensure the CLI path produces complete translated output
- keep mock mode unchanged

## Constraints
- Follow AGENTS.md and .codex/config.toml
- no cloud APIs
- no model download
- CPU only
- preserve current architecture as much as possible

## Deliverables
- fix in CT2 engine path or pipeline if needed
- regression test covering the TXT sample
- minimal docs update if behavior/config changes

## Validation
- pytest -q
- ruff check .
- mypy packages
- manual CLI run on tests/fixtures/text/plain_sample.txt must preserve both translated sentences

## Out of scope
- cloud APIs
- GPU-specific optimization

## Imported issue body
## Goal
Ensure real CLI translation with Marian/OPUS-MT preserves the full source content and produces complete output.

## Context
The CLI could run real local CT2 translation with a Marian model and local tokenizer, but output fidelity was incorrect on a simple TXT fixture:
- source: two sentences
- output: only one translated sentence

## Scope
- investigate tokenizer and decoding behavior for Marian/OPUS-MT
- compare current engine behavior with the standalone smoke test
- ensure the CLI path produces complete translated output
- keep mock mode unchanged

## Constraints
- no cloud APIs
- no model download
- CPU only
- preserve current architecture as much as possible

## Deliverables
- fix in CT2 engine path or pipeline if needed
- regression test covering the TXT sample
- minimal docs update if behavior/config changes

## Validation
- pytest -q
- ruff check .
- mypy packages
- manual CLI run on tests/fixtures/text/plain_sample.txt must preserve both translated sentences

## Completion checklist
- [x] code added
- [x] tests added
- [x] validation passed
- [x] docs updated
- [x] issue closure comment posted
