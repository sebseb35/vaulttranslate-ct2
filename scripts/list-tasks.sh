#!/usr/bin/env bash
set -euo pipefail

STATUS_FILE="docs/backlog-status.md"

if [[ ! -f "$STATUS_FILE" ]]; then
  echo "Missing $STATUS_FILE"
  exit 1
fi

awk '
  /^## Completed Catch-up/ { section=1; next }
  section == 1 && /^\| Work Item / { in_table=1; next }
  in_table && /^\|---/ { next }
  in_table && /^\|/ {
    gsub(/^\|[ ]*/, "");
    split($0, cols, "|");
    work=cols[1];
    task=cols[2];
    status=cols[3];
    follow_up=cols[5];
    gsub(/^ +| +$/, "", work);
    gsub(/^ +| +$/, "", task);
    gsub(/^ +| +$/, "", status);
    gsub(/^ +| +$/, "", follow_up);
    print status " | " work " | " task " | follow-up=" follow_up;
    next
  }
  in_table && !/^\|/ {
    in_table=0;
    section=0;
  }
' "$STATUS_FILE"
