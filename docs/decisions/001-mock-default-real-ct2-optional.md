# Decision 001: Mock Default, Real CT2 Optional

## Status
Accepted

## Context
The project needs deterministic local development, fast tests, and zero required model setup while still supporting real offline translation with CTranslate2.

## Decision
The default execution mode is the mock engine. Real CTranslate2 execution is enabled only when the user explicitly provides a local model path.

## Alternatives Considered
- Require a real CT2 model for all runs
- Hide the mock engine behind test-only code

## Consequences
- Local development and CI stay simple and deterministic
- Real translation remains possible without changing the core interfaces
- The CLI and docs must be explicit about the difference between mock mode and real CT2 mode
