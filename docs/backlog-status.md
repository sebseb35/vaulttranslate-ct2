# Backlog Status Snapshot

Last updated: 2026-04-05

This file is a local planning snapshot. GitHub Issues remain source of truth.

## Completed Catch-up

| Work Item | Task Contract | Status | Evidence | Follow-up Needed |
|---|---|---|---|---|
| Bootstrap core domain contracts | `docs/tasks/bootstrap-core.md` | done | core models/interfaces + tests merged (`579febd`) | no |
| CLI skeleton | `docs/tasks/cli-skeleton.md` | done | Typer CLI + entrypoint + tests (`bae47a8`) | no |
| TXT/MD adapter | `docs/tasks/text-adapter.md` | done | adapter extraction/rebuild + fixtures/tests (`bbcec0d`) | yes |
| CTranslate2 engine | `docs/tasks/engine-ct2.md` | done | CPU engine wrapper + tests (`9aa1906`) | yes |
| DOCX adapter | `docs/tasks/docx-adapter.md` | done | paragraph/run/table/header/footer support (`987f1ac`) | yes |
| Pipeline E2E wiring | `docs/tasks/pipeline-e2e.md` | done | CLI->adapter->engine->output flow (`3916180`) | no |
| Engine mode (mock + real) | `docs/tasks/engine-mode.md` | done | optional model-path mode + tests (`3765e50`) | no |
| Real CT2 smoke test | `docs/tasks/real-ct2-smoke-test.md` | done | optional local smoke validation (`4796253`) | yes |
| CT2 tokenizer integration | `docs/tasks/ct2-tokenizer-integration.md` | done | AutoTokenizer encode/decode flow (`d129d29`) | yes |
| Marian output fidelity fix | `docs/tasks/fix-marian-ct2-output-fidelity.md` | done | multiline preservation fix + regression (`380213d`) | yes |
| Integration + packaging | `docs/tasks/integration-packaging.md` | done | E2E integration tests + packaging/docs (`948f1f1`) | no |

## Recommended Next Priorities

| Priority | Candidate Issue Title | Type | Area | Why Next |
|---|---|---|---|---|
| P1 | Sentence-level chunking for long single-line CT2 inputs | tech-debt | engine | current fix is newline-based; long lines still risk truncation |
| P1 | Add PPTX adapter MVP | feature | adapter | supported format target not yet implemented |
| P1 | Add XLSX adapter MVP | feature | adapter | supported format target not yet implemented |
| P1 | Add PDF-text adapter MVP | feature | adapter | supported format target not yet implemented |
| P2 | Structured CT2 generation config (beam/max lengths) | research | engine | model-specific quality/stability tuning |
| P2 | CI matrix split: fast default + optional local CT2 checklist | quality | packaging | keeps deterministic CI while guiding real-model validation |
| P2 | CLI UX polish for progress and summary metadata | feature | cli | improves local operator experience |

## Close Immediately in GitHub

The following issue-equivalent backlog items can be marked closed if still open:
- bootstrap-core
- cli-skeleton
- text-adapter
- engine-ct2
- docx-adapter
- pipeline-e2e
- engine-mode
- real-ct2-smoke-test
- ct2-tokenizer-integration
- fix-marian-ct2-output-fidelity
- integration-packaging
