# Task: Fix Marian CT2 output fidelity

## Goal
Ensure real CLI translation with Marian/OPUS-MT preserves the full source content and produces complete output.

## Context
The current CLI can run real local CT2 translation with a Marian model and local tokenizer, but output fidelity is incorrect on a simple TXT fixture:
- source: two sentences
- output: only one translated sentence

## Requirements
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