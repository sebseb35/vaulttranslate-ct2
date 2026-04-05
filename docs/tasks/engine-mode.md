# Task: Engine mock + real mode

## Goal
Support both mock translation and optional real CTranslate2 usage.

## Requirements
- Default: mock translation (no model required)
- Optional: real engine when model_path is provided
- Keep TranslatorEngine interface unchanged

## Constraints
- no model download
- CPU only
- no cloud APIs
- no GPU assumptions

## Deliverables
- engine configuration improvements
- CLI integration (optional model path)
- tests for both modes
- minimal documentation update

## Validation
- pytest -q
- ruff check .
- mypy packages