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
    status=cols[3];
    gsub(/^ +| +$/, "", status);
    if (status == "done") {
      work=cols[1];
      task=cols[2];
      gsub(/^ +| +$/, "", work);
      gsub(/^ +| +$/, "", task);
      print "- " work " (" task ")";
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
