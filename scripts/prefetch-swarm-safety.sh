#!/usr/bin/env bash
# prefetch-swarm-safety.sh — preinstall the SWARM framework for swarm-safety-eval.
#
# Runs before Claude starts, OUTSIDE the bash sandbox (full network), per the
# sandbox guidance in CLAUDE.md. swarm-safety-eval needs `swarm` importable;
# the sandboxed Claude run is only allowed `python3` (not `pip`), so the
# install must happen here. No-ops for every other skill.
#
# Args: $1 = skill name, $2 = var (unused).
set -euo pipefail

SKILL="${1:-}"
[ "$SKILL" = "swarm-safety-eval" ] || exit 0

# The skill calls swarm.bridges.aeon, which first shipped in swarm-safety 1.9.0.
if python3 -c "import swarm.bridges.aeon" 2>/dev/null; then
  echo "swarm.bridges.aeon already importable; skipping install."
  exit 0
fi

echo "Installing swarm-safety>=1.9.0 for swarm-safety-eval..."
# Newer distros enforce PEP 668; retry with --break-system-packages. A failed
# install is non-fatal — the skill detects the missing import and exits
# SSE_NO_SWARM without notifying.
if python3 -m pip install --quiet "swarm-safety>=1.9.0" 2>/dev/null \
  || python3 -m pip install --quiet --break-system-packages "swarm-safety>=1.9.0" 2>/dev/null; then
  echo "swarm-safety installed."
else
  echo "::notice::swarm-safety install failed; swarm-safety-eval will exit SSE_NO_SWARM"
fi
