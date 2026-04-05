#!/usr/bin/env bash
set -euo pipefail

STATUS_FILE="docs/backlog-status.generated.md"

if [[ ! -f "$STATUS_FILE" ]]; then
  echo "Missing $STATUS_FILE"
  echo "Run: ./scripts/sync-backlog.sh"
  exit 1
fi

awk '
  /^## Closed Issues/ { section=1; next }
  section == 1 && /^\| Number / { in_table=1; next }
  in_table && /^\|---/ { next }
  in_table && /^\|/ {
    gsub(/^\|[ ]*/, "");
    split($0, cols, "|");
    number=cols[1];
    title=cols[2];
    task=cols[4];
    state=cols[5];
    gsub(/^ +| +$/, "", number);
    gsub(/^ +| +$/, "", title);
    gsub(/^ +| +$/, "", task);
    gsub(/^ +| +$/, "", state);
    if (state == "closed") {
      print "- " number " | " title " | task=" task;
      count++;
    }
    next
  }
  in_table && !/^\|/ {
    in_table=0;
    section=0;
  }
  END { print "Total completed: " (count+0) }
' "$STATUS_FILE"
