#!/usr/bin/env bash
set -euo pipefail

STATUS_FILE="docs/backlog-status.md"

if [[ ! -f "$STATUS_FILE" ]]; then
  echo "Missing $STATUS_FILE"
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
    title=cols[2];
    type=cols[3];
    gsub(/^ +| +$/, "", priority);
    gsub(/^ +| +$/, "", title);
    gsub(/^ +| +$/, "", type);
    print priority " -> " title " (" type ")";
    next
  }
  in_table && !/^\|/ {
    in_table=0;
    section=0;
  }
' "$STATUS_FILE"
