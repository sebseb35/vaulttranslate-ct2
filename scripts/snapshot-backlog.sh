#!/usr/bin/env bash
set -euo pipefail

OUT="docs/backlog-status.generated.md"

{
  echo "# Generated Backlog Snapshot"
  echo
  echo "Generated: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  echo
  echo "| Task Contract | Last Touch Commit |"
  echo "|---|---|"
  for f in $(find docs/tasks -maxdepth 1 -type f -name '*.md' | sort); do
    base="$(basename "$f")"
    if [[ "$base" == "_template.md" ]]; then
      continue
    fi
    commit="$(git log -n 1 --pretty=format:%h -- "$f" 2>/dev/null || true)"
    if [[ -z "$commit" ]]; then
      commit="n/a"
    fi
    echo "| $f | $commit |"
  done
} > "$OUT"

echo "Wrote $OUT"
