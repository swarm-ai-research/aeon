#!/usr/bin/env bash
#
# memory-checkpoint.sh — git-backed checkpoint/versioning for memory/ (hxmp.5)
#
# Ports fabro-checkpoint's branch-per-run model to Aeon. Each checkpoint is a
# commit on a dedicated `aeon-checkpoints` lineage whose tree contains ONLY the
# `memory/` directory, so the history is isolated from the main branch and grows
# monotonically (one commit per run). Every checkpoint also gets a human-readable
# tag, and carries provenance as commit trailers (run id, skill, timestamp).
#
# This lets memory state be rolled back to any prior run and lets agent forks
# branch off a known-good memory snapshot — without polluting main's history.
#
# Subcommands:
#   create [--skill NAME] [--run-id ID] [--run-url URL] [--no-tag]
#       Snapshot the current memory/ tree as a new checkpoint commit + tag.
#   list [-n N]
#       List checkpoints, newest first, with provenance.
#   show <ref>
#       Show a checkpoint's provenance and what changed vs its parent.
#   rollback <ref> [--force]
#       Restore the working tree's memory/ to the state at <ref>.
#   fork <ref> <new-branch> [--base BRANCH]
#       Create <new-branch> = base branch with memory/ swapped to <ref>.
#   prune --keep N
#       Drop all but the newest N checkpoints (commits + tags).
#
# <ref> may be a checkpoint tag (aeon/ckpt/...), a commit sha, or an offset like
# "@{2}" against the aeon-checkpoints branch.
#
# Env (used as provenance defaults by `create`, all optional):
#   AEON_CKPT_SKILL, GITHUB_RUN_ID, AEON_CKPT_RUN_URL
#
set -euo pipefail

CKPT_BRANCH="aeon-checkpoints"
CKPT_REF="refs/heads/${CKPT_BRANCH}"
TAG_PREFIX="aeon/ckpt"
MEMORY_DIR="memory"

die() { echo "memory-checkpoint: $*" >&2; exit 1; }

# Resolve repo root and operate from there so relative paths are stable.
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repository"
cd "$REPO_ROOT"

[ -d "$MEMORY_DIR" ] || die "no $MEMORY_DIR/ directory at repo root"

ckpt_tip() { git rev-parse -q --verify "$CKPT_REF" 2>/dev/null || true; }

# Resolve a user-supplied ref to a checkpoint commit sha. Accepts a tag, a raw
# sha, or a revision expression against the checkpoint branch (e.g. "@{1}").
resolve_ckpt() {
  local ref="$1" sha
  # Try as-is, then as an offset on the checkpoint branch.
  sha="$(git rev-parse -q --verify "${ref}^{commit}" 2>/dev/null || true)"
  [ -z "$sha" ] && sha="$(git rev-parse -q --verify "${CKPT_BRANCH}${ref}^{commit}" 2>/dev/null || true)"
  [ -z "$sha" ] && die "cannot resolve checkpoint ref: $ref"
  echo "$sha"
}

# Build a root tree object containing only memory/ from the current worktree,
# using a throwaway index so the real index is untouched.
memory_root_tree() {
  local tmpidx mem_tree
  tmpidx="$(mktemp)"
  # shellcheck disable=SC2064
  trap "rm -f '$tmpidx'" RETURN
  GIT_INDEX_FILE="$tmpidx" git read-tree --empty
  GIT_INDEX_FILE="$tmpidx" git add -A -- "$MEMORY_DIR"
  mem_tree="$(GIT_INDEX_FILE="$tmpidx" git write-tree)"
  echo "$mem_tree"
}

cmd_create() {
  local skill="${AEON_CKPT_SKILL:-}" run_id="${GITHUB_RUN_ID:-}" run_url="${AEON_CKPT_RUN_URL:-}" make_tag=1
  while [ $# -gt 0 ]; do
    case "$1" in
      --skill)   skill="$2"; shift 2 ;;
      --run-id)  run_id="$2"; shift 2 ;;
      --run-url) run_url="$2"; shift 2 ;;
      --no-tag)  make_tag=0; shift ;;
      *) die "create: unknown arg: $1" ;;
    esac
  done

  local root_tree parent at_iso at_compact
  root_tree="$(memory_root_tree)"
  parent="$(ckpt_tip)"

  # Skip if nothing changed since the last checkpoint (idempotent per state).
  if [ -n "$parent" ]; then
    local parent_tree
    parent_tree="$(git rev-parse "${parent}^{tree}")"
    if [ "$parent_tree" = "$root_tree" ]; then
      echo "No memory changes since last checkpoint ($(git rev-parse --short "$parent")); skipping."
      return 0
    fi
  fi

  at_iso="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  at_compact="$(date -u +%Y%m%dT%H%M%SZ)"

  # Assemble the commit message: subject + provenance trailers.
  local subject body
  subject="checkpoint: ${skill:-manual} @ ${at_iso}"
  body="$(printf '%s\n' "$subject" ""; \
    printf 'Aeon-Run-At: %s\n' "$at_iso"; \
    [ -n "$skill" ]   && printf 'Aeon-Skill: %s\n' "$skill"; \
    [ -n "$run_id" ]  && printf 'Aeon-Run-Id: %s\n' "$run_id"; \
    [ -n "$run_url" ] && printf 'Aeon-Run-Url: %s\n' "$run_url"; \
    printf 'Aeon-Parent: %s\n' "${parent:-root}")"

  local commit
  commit="$(printf '%s' "$body" | git commit-tree "$root_tree" ${parent:+-p "$parent"} -F -)"
  git update-ref "$CKPT_REF" "$commit" ${parent:+"$parent"}

  local tag=""
  if [ "$make_tag" -eq 1 ]; then
    local slug="${skill:-manual}"
    slug="$(printf '%s' "$slug" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-')"
    tag="${TAG_PREFIX}/${at_compact}-${slug}"
    # Disambiguate if two runs land in the same second.
    [ -n "$run_id" ] && ! git rev-parse -q --verify "refs/tags/$tag" >/dev/null 2>&1 || \
      tag="${tag}-${run_id:-$(git rev-parse --short "$commit")}"
    git tag -f "$tag" "$commit" >/dev/null
  fi

  echo "Created checkpoint $(git rev-parse --short "$commit")${tag:+ (tag: $tag)}"
}

cmd_list() {
  local limit=20
  while [ $# -gt 0 ]; do
    case "$1" in
      -n) limit="$2"; shift 2 ;;
      *) die "list: unknown arg: $1" ;;
    esac
  done
  [ -n "$(ckpt_tip)" ] || { echo "No checkpoints yet."; return 0; }

  [ -n "$(git tag --list "${TAG_PREFIX}/*")" ] || { echo "No checkpoints yet."; return 0; }

  printf '%-9s  %-20s  %-22s  %-10s  %s\n' "COMMIT" "WHEN (UTC)" "SKILL" "RUN ID" "TAG"
  # Checkpoints are the per-run tags; the aeon-checkpoints branch is the durable
  # store beneath them. for-each-ref sorts/selects the tags, but we read the
  # provenance fields through `git log -1` because only the log/show formatter
  # interprets %xNN escapes and the trailers `separator=` (which suppresses the
  # atom's automatic trailing newline, keeping each record on one line).
  git for-each-ref --sort=-creatordate --count="$limit" \
    --format='%(refname:short)' "refs/tags/${TAG_PREFIX}" \
  | while IFS= read -r tag; do
      local line sha at skill run
      line="$(git log -1 \
        --format='%h%x1f%(trailers:key=Aeon-Run-At,valueonly,separator=%x00)%x1f%(trailers:key=Aeon-Skill,valueonly,separator=%x00)%x1f%(trailers:key=Aeon-Run-Id,valueonly,separator=%x00)' \
        "$tag")"
      IFS=$'\x1f' read -r sha at skill run <<EOF
$line
EOF
      printf '%-9s  %-20s  %-22s  %-10s  %s\n' "$sha" "${at:0:19}" "${skill:-manual}" "${run:--}" "$tag"
    done
}

cmd_show() {
  [ $# -ge 1 ] || die "show: need a <ref>"
  local sha; sha="$(resolve_ckpt "$1")"
  git --no-pager show --no-patch --format='commit %H%nsubject: %s%n%n%b' "$sha"
  echo "--- memory/ changes vs parent ---"
  local parent; parent="$(git rev-parse -q --verify "${sha}^" 2>/dev/null || true)"
  if [ -n "$parent" ]; then
    git --no-pager diff --stat "$parent" "$sha" -- "$MEMORY_DIR" || true
  else
    git --no-pager show --stat --oneline "$sha" | tail -n +2
  fi
}

cmd_rollback() {
  [ $# -ge 1 ] || die "rollback: need a <ref>"
  local ref="$1" force=0; shift
  while [ $# -gt 0 ]; do
    case "$1" in --force) force=1; shift ;; *) die "rollback: unknown arg: $1" ;; esac
  done
  local sha; sha="$(resolve_ckpt "$ref")"

  if [ "$force" -ne 1 ]; then
    if ! git diff --quiet -- "$MEMORY_DIR" || ! git diff --cached --quiet -- "$MEMORY_DIR"; then
      die "$MEMORY_DIR/ has uncommitted changes; commit/stash them or pass --force"
    fi
  fi

  # Materialize exactly the checkpoint's memory tree (removes files added since).
  rm -rf "$MEMORY_DIR"
  git checkout "$sha" -- "$MEMORY_DIR"
  echo "Rolled back $MEMORY_DIR/ to checkpoint $(git rev-parse --short "$sha")."
  echo "Review with 'git status' / 'git diff --cached', then commit to keep it."
}

cmd_fork() {
  [ $# -ge 2 ] || die "fork: need <ref> <new-branch>"
  local ref="$1" branch="$2" base="main"; shift 2
  while [ $# -gt 0 ]; do
    case "$1" in --base) base="$2"; shift 2 ;; *) die "fork: unknown arg: $1" ;; esac
  done
  git rev-parse -q --verify "refs/heads/$branch" >/dev/null 2>&1 && die "branch already exists: $branch"
  local ckpt base_commit mem_tree tmpidx new_tree fork_commit
  ckpt="$(resolve_ckpt "$ref")"
  base_commit="$(git rev-parse -q --verify "${base}^{commit}")" || die "no such base branch: $base"
  mem_tree="$(git rev-parse -q --verify "${ckpt}:${MEMORY_DIR}")" || die "checkpoint has no $MEMORY_DIR tree"

  tmpidx="$(mktemp)"
  # shellcheck disable=SC2064
  trap "rm -f '$tmpidx'" RETURN
  GIT_INDEX_FILE="$tmpidx" git read-tree "${base_commit}^{tree}"
  GIT_INDEX_FILE="$tmpidx" git rm -r --cached --ignore-unmatch -- "$MEMORY_DIR" >/dev/null
  GIT_INDEX_FILE="$tmpidx" git read-tree --prefix="${MEMORY_DIR}/" "$mem_tree"
  new_tree="$(GIT_INDEX_FILE="$tmpidx" git write-tree)"
  fork_commit="$(git commit-tree "$new_tree" -p "$base_commit" \
    -m "fork: ${MEMORY_DIR}/ from checkpoint $(git rev-parse --short "$ckpt") onto ${base}")"
  git update-ref "refs/heads/$branch" "$fork_commit"
  echo "Created fork branch '$branch' = ${base} with ${MEMORY_DIR}/ from $(git rev-parse --short "$ckpt")."
  echo "Check it out with: git checkout $branch"
}

cmd_prune() {
  local keep=""
  while [ $# -gt 0 ]; do
    case "$1" in --keep) keep="$2"; shift 2 ;; *) die "prune: unknown arg: $1" ;; esac
  done
  [ -n "$keep" ] || die "prune: --keep N is required"
  case "$keep" in ''|*[!0-9]*) die "prune: --keep needs a non-negative integer" ;; esac

  local total
  total="$(git for-each-ref --format='x' "refs/tags/${TAG_PREFIX}" | wc -l | tr -d ' ')"
  if [ "$total" -le "$keep" ]; then
    echo "$total checkpoint(s); keeping $keep — nothing to prune."
    return 0
  fi

  # Newest-first; delete everything past the first $keep. The aeon-checkpoints
  # branch (the durable store) is left intact, so a pruned tag's commit is still
  # reachable by sha until a later compaction.
  local i=0 deleted=0
  while IFS= read -r t; do
    i=$((i + 1))
    if [ "$i" -gt "$keep" ]; then
      git tag -d "$t" >/dev/null && deleted=$((deleted + 1))
    fi
  done < <(git for-each-ref --sort=-creatordate --format='%(refname:short)' "refs/tags/${TAG_PREFIX}")
  echo "Pruned $deleted old checkpoint tag(s); kept newest $keep."
}

usage() {
  sed -n '2,40p' "$0" | sed 's/^# \{0,1\}//'
}

[ $# -ge 1 ] || { usage; exit 1; }
sub="$1"; shift
case "$sub" in
  create)   cmd_create "$@" ;;
  list)     cmd_list "$@" ;;
  show)     cmd_show "$@" ;;
  rollback) cmd_rollback "$@" ;;
  fork)     cmd_fork "$@" ;;
  prune)    cmd_prune "$@" ;;
  -h|--help|help) usage ;;
  *) die "unknown subcommand: $sub (try --help)" ;;
esac
