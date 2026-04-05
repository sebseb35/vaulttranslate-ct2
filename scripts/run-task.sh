#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: scripts/run-task.sh <task-file>"
  exit 1
fi

TASK_FILE="$1"

if [[ ! -f "$TASK_FILE" ]]; then
  echo "Task file not found: $TASK_FILE"
  exit 1
fi

codex "Implement ${TASK_FILE}.
Follow AGENTS.md and .codex/config.toml.
Workflow:
1) inspect repository and propose a short plan
2) implement with tests
3) run validation (pytest -q, ruff check ., mypy packages)
4) summarize risks and next follow-ups."
