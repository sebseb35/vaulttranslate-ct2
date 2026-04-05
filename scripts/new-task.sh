#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: scripts/new-task.sh <issue_number> [slug]"
  exit 1
fi

ISSUE_RAW="$1"
ISSUE="${ISSUE_RAW#\#}"
SLUG_INPUT="${2:-}"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required."
  exit 1
fi

TITLE="$(gh issue view "$ISSUE" --json title --jq '.title')"
BODY="$(gh issue view "$ISSUE" --json body --jq '.body // ""')"

if [[ -n "$SLUG_INPUT" ]]; then
  SLUG="$SLUG_INPUT"
else
  SLUG="$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"
fi

if ! [[ "$ISSUE" =~ ^[0-9]+$ ]]; then
  echo "Issue must be numeric (example: 42 or #42)"
  exit 1
fi

PADDED_ISSUE="$(printf "%03d" "$ISSUE")"
OUT="docs/tasks/${PADDED_ISSUE}-${SLUG}.md"

if [[ -f "$OUT" ]]; then
  echo "Task already exists: $OUT"
  exit 1
fi

cat > "$OUT" <<EOF
# Task

## Metadata
- Issue: #$ISSUE
- Status: ready
- Priority: P2
- Type: feature
- Area: core

## Title
$TITLE

## Goal
Describe what should exist when this task is done.

## Context
Imported from issue #$ISSUE.

## Scope
- item
- item

## Constraints
- Follow AGENTS.md and .codex/config.toml
- No new dependency unless justified
- Add or update tests

## Deliverables
- implementation
- tests
- docs update if needed

## Validation
- pytest -q
- ruff check .
- mypy packages

## Out of scope
- item
- item

## Imported issue body
$BODY

## Completion checklist
- [ ] code added
- [ ] tests added
- [ ] validation passed
- [ ] docs updated
- [ ] issue closure comment posted
EOF

echo "Created $OUT from issue #$ISSUE"
