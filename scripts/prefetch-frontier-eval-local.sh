#!/usr/bin/env bash
# Gated entrypoint for the frontier-eval local-models track. Same gate pattern
# as prefetch-frontier-eval.sh: the workflow's generic loop calls every
# prefetch-*.sh for every skill, so we exit 0 unless this is the frontier-eval
# skill firing. When the gate passes, exec the .mjs that talks to Ollama.
#
# Local-track is opt-in via OLLAMA_HOST being reachable. If Ollama isn't
# running, the .mjs exits cleanly itself — no need to probe at the shell.

set -euo pipefail

SKILL="${1:-}"
if [ "$SKILL" != "frontier-eval" ]; then
  exit 0
fi

exec node "$(dirname "$0")/frontier-eval-local-prefetch.mjs"
