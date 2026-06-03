#!/usr/bin/env bash
# Delete orphan `aeon/{docs,test,refactor}-pass-*` branches on origin that
# accumulated while the fleet-runner was missing GH_TOKEN (see PR #109): each
# code-pass pushed its branch BEFORE calling `gh pr create`, which then failed,
# leaving the branch behind with no PR.
#
# Safe-by-default:
#   - Dry-run unless --apply is passed.
#   - Skips any branch with an open PR (no in-flight work is touched).
#   - Lists the leading commit subject of every candidate so an operator can
#     spot-check before applying.
#
# Usage:
#   scripts/cleanup-orphan-pass-branches.sh              # dry-run, prints plan
#   scripts/cleanup-orphan-pass-branches.sh --apply      # actually delete
#
# Requires: gh CLI authenticated, working tree on a checkout of the repo.

set -euo pipefail

APPLY=0
if [[ "${1:-}" == "--apply" ]]; then APPLY=1; fi

git fetch --prune origin >/dev/null 2>&1

# Portable to bash 3 (macOS default) — no mapfile / no associative arrays.
CANDIDATES=()
while IFS= read -r line; do
  CANDIDATES+=("$line")
done < <(
  git branch -r |
    sed 's/^[[:space:]]*//' |
    grep -E '^origin/aeon/(docs|test|refactor)-pass-' |
    sed 's|^origin/||' |
    sort
)

if [[ ${#CANDIDATES[@]} -eq 0 ]]; then
  echo "No orphan code-pass branches found."
  exit 0
fi

# Snapshot every branch that currently backs an OPEN PR. The status filter is
# explicit (`--state open`) — closed PRs no longer protect their branch.
OPEN_PR_HEADS=$(gh pr list --state open --limit 500 --json headRefName -q '.[].headRefName' | tr '\n' '|')

to_delete=()
skipped=()
for branch in "${CANDIDATES[@]}"; do
  # `|branch|` lookup in the pipe-delimited snapshot — exact-match, no prefix hits.
  if [[ "|$OPEN_PR_HEADS|" == *"|$branch|"* ]]; then
    skipped+=("$branch")
    continue
  fi
  to_delete+=("$branch")
done

echo "Candidates: ${#CANDIDATES[@]}  ·  to delete: ${#to_delete[@]}  ·  skipped (open PR): ${#skipped[@]}"
echo

if [[ ${#to_delete[@]} -gt 0 ]]; then
  echo "Branches to delete (first line of leading commit):"
  for branch in "${to_delete[@]}"; do
    subject=$(git log -1 --format=%s "origin/$branch" 2>/dev/null | cut -c1-100)
    printf "  %s\n      %s\n" "$branch" "${subject:-<no commit found>}"
  done
  echo
fi

if [[ ${#skipped[@]} -gt 0 ]]; then
  echo "Skipped (open PR — left alone):"
  for branch in "${skipped[@]}"; do echo "  $branch"; done
  echo
fi

if [[ $APPLY -eq 0 ]]; then
  echo "Dry-run. Re-run with --apply to delete the ${#to_delete[@]} listed branches."
  exit 0
fi

echo "Applying — deleting ${#to_delete[@]} branches on origin…"
fail=0
for branch in "${to_delete[@]}"; do
  if git push origin --delete "$branch" >/dev/null 2>&1; then
    echo "  deleted: $branch"
  else
    echo "  FAILED:  $branch"
    fail=$((fail + 1))
  fi
done

echo
if [[ $fail -gt 0 ]]; then
  echo "Done with $fail failure(s)."
  exit 1
fi
echo "Done. Deleted ${#to_delete[@]} orphan branches."
