# Decision 002: PDF Support Is Text-First and No-OCR

## Status
Accepted

## Context
PDF is an important enterprise format, but visually faithful reconstruction and OCR both add significant complexity and risk for an MVP-oriented offline pipeline.

## Decision
PDF support is limited to text-based PDFs. Extraction is text-first, rebuild output is a simple readable PDF, and OCR is out of scope.

## Alternatives Considered
- Promise visual fidelity for PDFs
- Add OCR support in the initial PDF adapter

## Consequences
- PDF support is useful early without overcommitting on layout fidelity
- Scanned PDFs and visually complex PDFs are intentionally unsupported
- Product messaging and README wording must avoid implying pixel-perfect PDF preservation
