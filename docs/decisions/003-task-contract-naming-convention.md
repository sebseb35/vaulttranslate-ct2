# Decision 003: Task Contracts Use `NNN-MMM-slug.md`

## Status
Accepted

## Context
The repository mixes historical task contracts and newer issue-backed tasks. A consistent naming scheme is needed so backlog tooling, task discovery, and issue mapping stay predictable.

## Decision
Task contracts use the `docs/tasks/NNN-MMM-slug.md` format, where `NNN` is the issue number and `MMM` is the previous sequence slot used to preserve stable ordering for imported legacy work.

## Alternatives Considered
- Keep mixing numbered and non-numbered task files
- Use a single-prefix `NNN-slug.md` convention

## Consequences
- Task files sort in a stable, explicit way
- Helper scripts and templates must reference the same naming convention
- Historical tasks can be brought into the same convention without losing ordering context
