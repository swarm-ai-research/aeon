#!/usr/bin/env bash
# sync-aeon-private.sh
#
# Phase 1 dual-write helper for the aeon ↔ aeon-private migration. After a
# workflow has done its real work and committed to aeon as usual, this script
# mirrors the operational state directories (memory/, articles/, soul/,
# dashboard/outputs/) over to rsavitt/aeon-private. The mirror is the secondary
# write — aeon remains source of truth during Phase 1.
#
# Safe to call from any workflow as a post-step. Always exits 0 so a sync
# failure never breaks the main job.
#
# Requires AEON_PRIVATE_PAT in env (fine-grained PAT with contents:write on
# rsavitt/aeon-private). If absent, this script no-ops with a log line — that
# makes it safe to land before the secret is rolled out.
#
# Remove this script (and the workflow post-steps that invoke it) at Phase 2
# cutover, when aeon's working tree no longer holds the mirrored directories.

set -uo pipefail

if [ -z "${AEON_PRIVATE_PAT:-}" ]; then
  echo "[sync-aeon-private] AEON_PRIVATE_PAT not set — skipping (dual-write off)"
  exit 0
fi

REPO_DIR="${GITHUB_WORKSPACE:-$PWD}"
PRIVATE_DIR="${RUNNER_TEMP:-/tmp}/aeon-private-sync"
PRIVATE_URL="https://x-access-token:${AEON_PRIVATE_PAT}@github.com/rsavitt/aeon-private.git"
MIRRORED_DIRS=(memory articles soul dashboard/outputs)

# Refuse to mirror when aeon's working tree has commits that never made it to
# origin/main — that path arises when the workflow's own commit/push step
# exhausted its retries (cron-state push concurrency, message-volume races,
# etc.). Mirroring local-only commits would put state on aeon-private that
# never reaches aeon, breaking the "aeon is source of truth during Phase 1"
# invariant. Skip cleanly; the next successful run will catch up.
#
# Note: this guard only catches local-only COMMITS. Working-tree files staged
# via `git checkout <other-branch> -- <path>` (e.g. fleet-runner.yml overlays
# memory/gitlawb-compute-futures-proofs/ from origin/fleet-state) don't create
# commits and pass through to aeon-private intentionally — fleet-state content
# is durably committed on its own branch, and aeon-private is meant to mirror
# the combined operational view that skills actually read at runtime.
if [ -d "$REPO_DIR/.git" ]; then
  ( cd "$REPO_DIR" && git fetch origin main --depth=1 --quiet 2>/dev/null ) || true
  local_head=$( cd "$REPO_DIR" && git rev-parse HEAD 2>/dev/null || echo "" )
  remote_head=$( cd "$REPO_DIR" && git rev-parse origin/main 2>/dev/null || echo "" )
  if [ -n "$local_head" ] && [ -n "$remote_head" ] && [ "$local_head" != "$remote_head" ]; then
    # Allow the case where local is BEHIND remote (clean) — only refuse when
    # local has commits AHEAD of remote that aren't reachable from origin/main.
    ahead=$( cd "$REPO_DIR" && git rev-list --count "origin/main..HEAD" 2>/dev/null || echo "0" )
    if [ "$ahead" != "0" ]; then
      echo "[sync-aeon-private] local HEAD has $ahead unpushed commit(s) vs origin/main — skipping mirror (primary write didn't land; will retry next run)"
      exit 0
    fi
  fi
fi

# Clone fresh each run — shallow clone is small (~1MB total state),
# and a fresh clone avoids stale-checkout races between concurrent jobs.
rm -rf "$PRIVATE_DIR"
if ! git clone --depth=1 --quiet "$PRIVATE_URL" "$PRIVATE_DIR" 2>/dev/null; then
  echo "[sync-aeon-private] clone failed — skipping this run"
  exit 0
fi

cd "$PRIVATE_DIR" || {
  echo "[sync-aeon-private] cd to $PRIVATE_DIR failed — skipping this run"
  exit 0
}
git config user.name "aeonframework"
git config user.email "aeonframework@proton.me"

# Mirror each tracked directory. No --delete: aeon is still source of truth
# during Phase 1, so a missing file on the aeon side shouldn't wipe history
# on the private side. The Phase 2 cutover PR will switch to authoritative
# write with delete semantics.
for d in "${MIRRORED_DIRS[@]}"; do
  if [ -d "$REPO_DIR/$d" ]; then
    mkdir -p "$PRIVATE_DIR/$d"
    rsync -a "$REPO_DIR/$d/" "$PRIVATE_DIR/$d/"
  fi
done

git add -A
if git diff --staged --quiet; then
  echo "[sync-aeon-private] no state changes to mirror"
  exit 0
fi

WF="${GITHUB_WORKFLOW:-local}"
RUN="${GITHUB_RUN_ID:-no-run}"
COMMIT_MSG="mirror: ${WF} run ${RUN} @ $(date -u +%FT%TZ)"
git commit --quiet -m "$COMMIT_MSG" || {
  echo "[sync-aeon-private] commit failed — skipping"
  exit 0
}

# Retry on concurrent-write races. Three rebase+push attempts is enough for
# the levels of concurrency we see (≤16 parallel skills via aeon.yml).
for attempt in 1 2 3; do
  if git push --quiet 2>/dev/null; then
    echo "[sync-aeon-private] mirrored: ${COMMIT_MSG}"
    exit 0
  fi
  git pull --rebase --autostash --quiet 2>/dev/null || true
done

echo "[sync-aeon-private] push failed after 3 attempts — will retry next run"
exit 0
