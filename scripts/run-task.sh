#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: scripts/run-task.sh <task-file>"
  exit 1
fi

TASK_FILE="$1"

codex "Implement the task described in ${TASK_FILE}. Follow AGENTS.md and .codex/config.toml. Inspect the repository first, then implement, test, and summarize risks."
