#!/usr/bin/env bash
set -euo pipefail

OUT="docs/backlog-status.generated.md"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required."
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not authenticated. Run: gh auth login"
  exit 1
fi

{
  echo "# Generated Backlog Status"
  echo
  echo "Generated: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  echo
  echo "GitHub Issues are the source of truth."
  echo
  echo "## Open Issues"
  echo
  echo "| Number | Title | Labels | Task File | State |"
  echo "|---|---|---|---|---|"

  gh issue list --state open --limit 200 --json number,title,labels | jq -r '
    .[] |
    [
      .number,
      .title,
      (.labels | map(.name) | join(", "))
    ] | @tsv
  ' | while IFS=$'\t' read -r number title labels; do
    task_file=$(find docs/tasks -maxdepth 1 -type f -name "$(printf "%03d" "$number")-*.md" | sort | head -n 1 || true)
    if [[ -z "${task_file:-}" ]]; then
      task_file="—"
    fi
    echo "| #$number | $title | $labels | $task_file | open |"
  done

  echo
  echo "## Closed Issues"
  echo
  echo "| Number | Title | Labels | Task File | State |"
  echo "|---|---|---|---|---|"

  gh issue list --state closed --limit 200 --json number,title,labels | jq -r '
    .[] |
    [
      .number,
      .title,
      (.labels | map(.name) | join(", "))
    ] | @tsv
  ' | while IFS=$'\t' read -r number title labels; do
    task_file=$(find docs/tasks -maxdepth 1 -type f -name "$(printf "%03d" "$number")-*.md" | sort | head -n 1 || true)
    if [[ -z "${task_file:-}" ]]; then
      task_file="—"
    fi
    echo "| #$number | $title | $labels | $task_file | closed |"
  done

  echo
  echo "## Recommended Next Priorities"
  echo
  echo "| Priority | Number | Title | Labels | Task File |"
  echo "|---|---|---|---|---|"

  gh issue list --state open --limit 200 --json number,title,labels | jq -r '
    .[]
    | .labels as $labels
    | [
        (
          if ($labels | map(.name) | index("P0")) then "P0"
          elif ($labels | map(.name) | index("P1")) then "P1"
          elif ($labels | map(.name) | index("P2")) then "P2"
          else "P9"
          end
        ),
        .number,
        .title,
        ($labels | map(.name) | join(", "))
      ] | @tsv
  ' | sort -t$'\t' -k1,1 -k2,2n | while IFS=$'\t' read -r priority number title labels; do
    task_file=$(find docs/tasks -maxdepth 1 -type f -name "$(printf "%03d" "$number")-*.md" | sort | head -n 1 || true)
    if [[ -z "${task_file:-}" ]]; then
      task_file="—"
    fi
    echo "| $priority | #$number | $title | $labels | $task_file |"
  done
} > "$OUT"

echo "Wrote $OUT"
