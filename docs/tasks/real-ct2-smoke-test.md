# Task: Real CTranslate2 smoke test

## Goal
Validate the full pipeline with a real local CTranslate2 model.

## Requirements
- Download a small compatible CT2 model manually
- Run CLI with --model-path
- Translate a sample txt and md file
- Verify output is produced and readable

## Scope
- No performance optimization
- No batching optimization
- No GPU
- No production hardening

## Constraints
- CPU only
- no automatic model download
- keep setup simple

## Deliverables
- working example with real model
- minimal documentation on how to place model
- optional small test or script

## Validation
- manual run success
- output file generated correctly