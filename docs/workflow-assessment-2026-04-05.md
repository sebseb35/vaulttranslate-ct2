# Workflow Assessment (2026-04-05)

## Scope
Audit of repository readiness for a pragmatic agentic workflow using:
- GitHub Issues as source of truth
- Codex Cloud for execution
- VS Code + Ubuntu for local development

## Observed baseline
- Existing AGENTS.md with product and implementation constraints.
- Existing Makefile with install/lint/type/test and backlog helper targets.
- Existing issue and PR templates under `.github/`.
- Existing lightweight agentic workflow document and task contracts under `docs/tasks/`.
- Existing scripts for task generation/execution and backlog sync.
- Existing test + lint + mypy tooling configured in `pyproject.toml`.

## Primary friction found
1. Inconsistent label parsing in backlog scripts (`P0/P1/P2` expected by script, `priority:P*` documented in workflow).
2. No CI workflow files under `.github/workflows/`, so canonical checks are not automatically enforced on PRs.
3. Task contracts generated from issues are only partially structured and keep placeholders (goal/scope/out-of-scope), reducing immediate agent execution quality.
4. Two issue templates overlap and can fragment authoring practices.
5. Makefile lacks explicit `verify` aggregate target and local setup bootstrap target naming convention.

## Recommended minimum target state
- Keep one canonical issue template for executable tasks.
- Keep `docs/tasks/` only for repeatable, implementation-oriented contracts.
- Add CI workflow with default gates: ruff + mypy + pytest.
- Add stable command interface (`setup`, `test`, `lint`, `typecheck`, `verify`, `tasks-*`).
- Normalize label taxonomy between docs/templates/scripts.

## Suggested implementation sequence
1. Align labels and backlog sync script parsing.
2. Add minimal CI workflow.
3. Add Makefile aliases (`typecheck`, `verify`, `setup`).
4. Tighten task template defaults for acceptance criteria and validation output.
5. Keep docs concise and link-driven to avoid documentation sprawl.
