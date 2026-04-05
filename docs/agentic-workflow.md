# Agentic Development Workflow

This repository uses a lightweight agentic workflow where:
- GitHub Issues are the backlog source of truth (why/what/priority)
- `docs/tasks/*.md` are executable implementation contracts (how)
- Codex executes tasks against the contract
- Human review decides merge/closure

## Operating Model

### Backlog
- Capture work in GitHub Issues first.
- Every implementation issue should map to one task contract in `docs/tasks/`.
- Use labels for triage and planning (see taxonomy below).

### Execution
- Create or update a task contract from the issue.
- Run Codex against the task contract.
- Keep changes small, tested, and validated (`pytest -q`, `ruff check .`, `mypy packages`).

### Delivery
- Open PR with concise summary, risks, and validation output.
- Ensure issue/task mapping is explicit in PR body.
- Keep docs in sync when conventions/interfaces change.

### Closure
- Close issue only when:
  - acceptance criteria are met
  - tests and validation pass
  - task contract checklist is complete
  - close comment is posted (template in `docs/templates/issue-close-comment.md`)

## Issue Lifecycle
1. `status:ready` - clarified and prioritized
2. `status:in-progress` - actively implemented
3. `status:blocked` - waiting on dependency/decision
4. `status:done` - merged and closed

## Label Taxonomy
Use a minimal, composable label set.

### Priority
- `priority:P0` critical
- `priority:P1` high
- `priority:P2` normal

### Type
- `type:bug`
- `type:feature`
- `type:tech-debt`
- `type:research`

### Area
- `area:core`
- `area:cli`
- `area:engine`
- `area:adapter`
- `area:packaging`
- `area:quality`
- `area:docs`

### Status
- `status:ready`
- `status:in-progress`
- `status:blocked`
- `status:done`

## Task Contract Convention (`docs/tasks`)

### Naming
- Task files should use: `docs/tasks/NNN-MMM-slug.md`
  - `NNN` is the GitHub issue number when available.
  - `MMM` is the previous sequence slot to preserve stable ordering with imported legacy tasks.
  - For issue `1`, use `000` as the second prefix.

### Structure
- Use `docs/tasks/_template.md`.
- Include issue reference and status metadata.
- Keep task contracts actionable and testable.

## Cadence
- Weekly 20-minute backlog review:
  - close completed issues
  - re-prioritize `status:ready`
  - identify blocked work and unblock plan
- After each merge:
  - update `docs/backlog-status.md`
  - post close comment in the issue

## Lightweight Local Commands
- Create task from issue: `scripts/new-task.sh <issue_number> [slug]`
- Run task with Codex: `scripts/run-task.sh docs/tasks/<task>.md`
- List all task statuses: `scripts/list-tasks.sh`
- List pending backlog items: `scripts/list-pending-tasks.sh`
- List completed backlog items: `scripts/summarize-completed-tasks.sh`
- Generate snapshot from current task files: `scripts/snapshot-backlog.sh`

## Decision Rules
- Prefer smallest change that satisfies the contract.
- Keep architecture stable unless issue explicitly requests change.
- Avoid new dependencies unless justified in issue/task.
- Keep real CT2 usage optional/local; default remains deterministic mock mode.
