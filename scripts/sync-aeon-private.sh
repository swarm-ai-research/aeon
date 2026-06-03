#!/usr/bin/env bash
# sync-aeon-private.sh
#
# Optional state-mirror helper. After a workflow has committed to the main
# repo as usual, this script mirrors operational state directories (memory/,
# articles/, soul/, dashboard/outputs/) over to a separate private mirror
# repo, if one is configured.
#
# Safe to call from any workflow as a post-step. Always exits 0 so a sync
# failure never breaks the main job. No-ops cleanly if env vars are unset,
# so it's a no-op for any fork that doesn't opt in.
#
# Required env vars to activate:
#   STATE_MIRROR_PAT  — fine-grained PAT with contents:write on the mirror repo
#   STATE_MIRROR_REPO — owner/repo of the mirror (e.g. "you/your-state-mirror")
#
# Without both, this script is a no-op.

set -uo pipefail

if [ -z "${STATE_MIRROR_PAT:-${AEON_PRIVATE_PAT:-}}" ] || [ -z "${STATE_MIRROR_REPO:-}" ]; then
  echo "[state-mirror] not configured — skipping"
  exit 0
fi

PAT="${STATE_MIRROR_PAT:-$AEON_PRIVATE_PAT}"
REPO_DIR="${GITHUB_WORKSPACE:-$PWD}"
PRIVATE_DIR="${RUNNER_TEMP:-/tmp}/state-mirror-sync"
PRIVATE_URL="https://x-access-token:${PAT}@github.com/${STATE_MIRROR_REPO}.git"
MIRRORED_DIRS=(memory articles soul dashboard/outputs)

# Refuse to mirror when the working tree has commits that never made it to
# origin/main — that path arises when the workflow's own commit/push step
# exhausted its retries. Mirroring local-only commits would put state on the
# mirror that never reaches the main repo. Skip cleanly; next run catches up.
if [ -d "$REPO_DIR/.git" ]; then
  ( cd "$REPO_DIR" && git fetch origin main --depth=1 --quiet 2>/dev/null ) || true
  local_head=$( cd "$REPO_DIR" && git rev-parse HEAD 2>/dev/null || echo "" )
  remote_head=$( cd "$REPO_DIR" && git rev-parse origin/main 2>/dev/null || echo "" )
  if [ -n "$local_head" ] && [ -n "$remote_head" ] && [ "$local_head" != "$remote_head" ]; then
    ahead=$( cd "$REPO_DIR" && git rev-list --count "origin/main..HEAD" 2>/dev/null || echo "0" )
    if [ "$ahead" != "0" ]; then
      echo "[state-mirror] local HEAD has $ahead unpushed commit(s) vs origin/main — skipping mirror"
      exit 0
    fi
  fi
fi

rm -rf "$PRIVATE_DIR"
if ! git clone --depth=1 --quiet "$PRIVATE_URL" "$PRIVATE_DIR" 2>/dev/null; then
  echo "[state-mirror] clone failed — skipping this run"
  exit 0
fi

cd "$PRIVATE_DIR" || {
  echo "[state-mirror] cd to $PRIVATE_DIR failed — skipping this run"
  exit 0
}
git config user.name "${GIT_AUTHOR_NAME:-state-mirror-bot}"
git config user.email "${GIT_AUTHOR_EMAIL:-state-mirror-bot@users.noreply.github.com}"

# Mirror each tracked directory. No --delete: a missing file on the main side
# shouldn't wipe history on the mirror side.
for d in "${MIRRORED_DIRS[@]}"; do
  if [ -d "$REPO_DIR/$d" ]; then
    mkdir -p "$PRIVATE_DIR/$d"
    rsync -a "$REPO_DIR/$d/" "$PRIVATE_DIR/$d/"
  fi
done

git add -A
if git diff --staged --quiet; then
  echo "[state-mirror] no state changes to mirror"
  exit 0
fi

WF="${GITHUB_WORKFLOW:-local}"
RUN="${GITHUB_RUN_ID:-no-run}"
COMMIT_MSG="mirror: ${WF} run ${RUN} @ $(date -u +%FT%TZ)"
git commit --quiet -m "$COMMIT_MSG" || {
  echo "[state-mirror] commit failed — skipping"
  exit 0
}

for attempt in 1 2 3; do
  if git push --quiet 2>/dev/null; then
    echo "[state-mirror] mirrored: ${COMMIT_MSG}"
    exit 0
  fi
  git pull --rebase --autostash --quiet 2>/dev/null || true
done

echo "[state-mirror] push failed after 3 attempts — will retry next run"
exit 0
