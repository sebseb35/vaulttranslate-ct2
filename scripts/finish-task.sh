#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: scripts/finish-task.sh <issue_number> <summary_file>"
  exit 1
fi

ISSUE_RAW="$1"
ISSUE="${ISSUE_RAW#\#}"
SUMMARY_FILE="$2"

if [[ ! -f "$SUMMARY_FILE" ]]; then
  echo "Summary file not found: $SUMMARY_FILE"
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required."
  exit 1
fi

echo "Commenting issue #$ISSUE..."
gh issue comment "$ISSUE" --body-file "$SUMMARY_FILE"

echo "Closing issue #$ISSUE..."
gh issue close "$ISSUE"

echo "Refreshing generated backlog snapshot..."
./scripts/sync-backlog.sh

echo "Done."
