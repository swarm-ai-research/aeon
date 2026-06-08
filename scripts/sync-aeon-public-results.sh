#!/usr/bin/env bash
# sync-aeon-public-results.sh
#
# Imports the latest outputs of public-mirror-side skills back into the
# private aeon's memory under memory/imports/. The public mirror at
# swarm-ai-research/aeon runs the 6 "public-safe" skills (compute-pulse,
# code-health, github-monitor, changelog, ai-framework-watch,
# compute-macro-correlate) on its own unlimited-Actions-minutes cron so
# the private fork doesn't burn private minutes on the same work; this
# script makes their outputs available to private-side consumers
# (planner, reflect, MOCs in memory/topics/).
#
# Reverse direction of scripts/sync-aeon-public.sh — that pushes
# framework + skills to public; this pulls public memory results back.
#
# Triggered by .github/workflows/sync-aeon-public-results.yml (daily cron
# + workflow_dispatch).
#
# Authentication: the public mirror is a public repo, so the clone is
# anonymous (no PAT needed). Commit + push back to private aeon uses
# the workflow's default GITHUB_TOKEN.
#
# Idempotency: the script no-ops cleanly if no files changed.

set -uo pipefail

REPO_DIR="${GITHUB_WORKSPACE:-$PWD}"
PUBLIC_DIR="${RUNNER_TEMP:-/tmp}/aeon-public-results"
PUBLIC_URL="https://github.com/swarm-ai-research/aeon.git"
IMPORTS_DIR="$REPO_DIR/memory/imports"

# Paths to import from the public mirror's memory/ and articles/ into
# private memory/imports/. Keep this list narrow — only the outputs of
# skills that were intentionally migrated. Adding more without a clear
# need clobbers private state silently.
#
# Format: each entry is "<source-path-relative-to-public-repo>::<dest-path-relative-to-private-imports>".
# A trailing slash on both sides copies the directory recursively.
IMPORTS=(
  'memory/topics/compute-pulse.md::compute-pulse.md'
  'memory/topics/external-prs.md::external-prs-public-view.md'
  'memory/topics/code-health.md::code-health.md'
  'memory/topics/ai-framework-watch.md::ai-framework-watch.md'
  'memory/topics/changelog.md::changelog.md'
  'memory/topics/compute-futures-macro-correlations.md::compute-futures-macro-correlations.md'
  # Second-wave migration (2026-06-07): pr-review tier moved to public.
  # Triage state files are the dedup source-of-truth — sync them back so
  # the operator can see triage history without browsing the public repo,
  # and so any future re-enable on private starts from current state.
  'memory/triaged-prs.json::triaged-prs.json'
  'memory/triaged-issues.json::triaged-issues.json'
  'memory/topics/pr-status.md::pr-status-public-view.md'
)

# Fresh shallow clone each run — public repo is small and a stale local
# checkout could race with the public-side scheduler's own commits.
rm -rf "$PUBLIC_DIR"
git clone --depth 1 "$PUBLIC_URL" "$PUBLIC_DIR" 2>&1 | tail -3

if [ ! -d "$PUBLIC_DIR/.git" ]; then
  echo "[sync-aeon-public-results] clone failed; aborting"
  exit 1
fi

mkdir -p "$IMPORTS_DIR"

# Touch the index so we can detect no-change cleanly even when files are
# absent on the public side.
INDEX_FILE="$IMPORTS_DIR/INDEX.md"
TMP_INDEX="$(mktemp)"
{
  echo "# Imports from swarm-ai-research/aeon"
  echo ""
  echo "*Auto-synced by \`scripts/sync-aeon-public-results.sh\`. Each entry below was the result of a public-mirror skill run as of the most recent sync. Do NOT hand-edit files in this directory — they get overwritten.*"
  echo ""
  echo "| Source (public) | Dest (private) | Status |"
  echo "|---|---|---|"
} > "$TMP_INDEX"

imported=0
missing=0

for spec in "${IMPORTS[@]}"; do
  src="${spec%%::*}"
  dst="${spec##*::}"
  src_abs="$PUBLIC_DIR/$src"
  dst_abs="$IMPORTS_DIR/$dst"

  if [ -e "$src_abs" ]; then
    mkdir -p "$(dirname "$dst_abs")"
    cp -R "$src_abs" "$dst_abs"
    echo "| \`$src\` | \`memory/imports/$dst\` | ✅ imported |" >> "$TMP_INDEX"
    imported=$((imported + 1))
  else
    echo "| \`$src\` | \`memory/imports/$dst\` | ⚠ missing on public |" >> "$TMP_INDEX"
    missing=$((missing + 1))
  fi
done

mv "$TMP_INDEX" "$INDEX_FILE"

# Detect change; bail cleanly if nothing moved.
cd "$REPO_DIR" || exit 1
if git diff --quiet memory/imports/; then
  echo "[sync-aeon-public-results] no changes (imported=$imported missing=$missing)"
  exit 0
fi

git config user.email "aeon-bot@users.noreply.github.com"
git config user.name "aeon-bot"
git add memory/imports/
git commit -m "sync-aeon-public-results: refresh imports ($imported files, $missing missing)" 2>&1 | tail -2
git push 2>&1 | tail -2

echo "[sync-aeon-public-results] committed imported=$imported missing=$missing"
