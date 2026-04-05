# AGENTS.md

## Project goal
Offline, secure document translation engine.

## Supported formats
DOCX, PPTX, XLSX, PDF (text), MD, TXT

## Constraints
- Fully offline
- No OCR (for now)
- No cloud APIs
- CPU-only execution
- Preserve document structure

## Allowed dependencies
- python-docx
- python-pptx
- openpyxl
- pdfplumber / pypdf
- CTranslate2

## Rules
- Write tests before/with code
- Do not introduce new dependencies without justification
- Keep modules decoupled
- Preserve formatting when possible

## Workflow
1. Plan
2. Tests
3. Implementation
4. Validation
5. Summary
