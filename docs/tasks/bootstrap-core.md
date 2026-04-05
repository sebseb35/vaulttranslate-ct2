# Task

## Title
Bootstrap core domain contracts

## Goal
Create the domain models and interfaces used by the translation pipeline.

## Context
This repo is an offline enterprise document translation engine supporting DOCX, PPTX, XLSX, PDF text, MD, and TXT.

## Scope
- add DocumentFormat enum
- add Segment and SegmentConstraints models
- add TranslationRequest and TranslationResult
- add abstract interfaces for TranslatorEngine and DocumentAdapter

## Constraints
- Python 3.12+
- use typed models
- no translation logic yet
- add unit tests

## Deliverables
- packages/core models
- interfaces
- tests

## Validation
- pytest
- ruff check .
- mypy packages

## Out of scope
- CTranslate2 integration
- document parsing
