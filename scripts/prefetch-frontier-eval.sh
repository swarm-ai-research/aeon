#!/usr/bin/env bash
# Gate the frontier-eval prefetch on the currently-running skill.
#
# The workflow runs every scripts/prefetch-*.sh before every skill and passes
# the skill name as $1. Without this gate, OPENROUTER_API_KEY + 6×50 model×task
# calls would fire for every cron, every day — burning the budget for skills
# that have nothing to do with frontier-eval.
#
# Real logic lives in scripts/frontier-eval-prefetch.mjs (renamed off the
# prefetch-*.sh glob on purpose).

set -euo pipefail

SKILL="${1:-}"
if [ "$SKILL" != "frontier-eval" ]; then
  exit 0
fi

exec node "$(dirname "$0")/frontier-eval-prefetch.mjs"
