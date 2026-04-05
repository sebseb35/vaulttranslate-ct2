# Task: Integrate Marian tokenizer into CT2 engine

## Goal
Enable real local translation through the CLI by integrating a proper tokenizer into the CTranslate2 engine.

## Context
The project already supports:
- mock translation (default)
- optional CTranslate2 engine via --model-path

However, the current engine uses a fallback whitespace tokenizer which is not compatible with real models such as Marian/OPUS-MT.

## Requirements
- load tokenizer with transformers.AutoTokenizer from a local directory or model reference
- encode input text using tokenizer.encode
- convert ids to tokens before passing to CTranslate2
- decode translated tokens back to text using the tokenizer
- keep compatibility with existing Segment and TranslationRequest structures

## Behavior
- if model_path is provided:
  - use tokenizer-based translation
- if no model_path:
  - keep mock engine unchanged

## Constraints
- no model download
- CPU only
- no cloud APIs
- keep tests deterministic (mock by default)
- real model usage must remain optional

## Deliverables
- tokenizer-aware CTranslate2 engine implementation
- minimal configuration (reuse model_path or optional tokenizer_path if needed)
- unit tests (mocked tokenizer/engine)
- optional small documentation update

## Validation
- pytest -q
- ruff check .
- mypy packages