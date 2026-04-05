#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: scripts/new-task.sh <slug> <issue_number>"
  exit 1
fi

SLUG="$1"
ISSUE="$2"
OUT="docs/tasks/${SLUG}.md"

gh issue view "$ISSUE" --json title,body --jq '"# Task\n\n## Title\n" + .title + "\n\n## Imported issue\n\n" + (.body // "")' > "$OUT"

echo "Created $OUT from issue #$ISSUE"
