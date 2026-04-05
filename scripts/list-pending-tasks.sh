#!/usr/bin/env bash
set -euo pipefail

STATUS_FILE="docs/backlog-status.generated.md"

if [[ ! -f "$STATUS_FILE" ]]; then
  echo "Missing $STATUS_FILE"
  echo "Run: ./scripts/sync-backlog.sh"
  exit 1
fi

awk '
  /^## Recommended Next Priorities/ { section=1; next }
  section == 1 && /^\| Priority / { in_table=1; next }
  in_table && /^\|---/ { next }
  in_table && /^\|/ {
    gsub(/^\|[ ]*/, "");
    split($0, cols, "|");
    priority=cols[1];
    number=cols[2];
    title=cols[3];
    labels=cols[4];
    task=cols[5];
    gsub(/^ +| +$/, "", priority);
    gsub(/^ +| +$/, "", number);
    gsub(/^ +| +$/, "", title);
    gsub(/^ +| +$/, "", labels);
    gsub(/^ +| +$/, "", task);
    print priority " -> " number " | " title " | task=" task " | labels=" labels;
    next
  }
  in_table && !/^\|/ {
    in_table=0;
    section=0;
  }
' "$STATUS_FILE"
