#!/usr/bin/env bash
# Pre-install workflow-security-audit scanner binaries OUTSIDE the Claude sandbox.
#
# workflow-security-audit uses zizmor and actionlint. On GitHub-hosted runners the
# in-sandbox install paths (pipx, pip, curl|bash) can be blocked by network policy.
# This script runs in the workflow's prefetch phase (aeon.yml loops prefetch-*.sh
# before Claude starts, with full network access). It seeds binaries into .audit-bin/;
# the skill exports PATH="$PWD/.audit-bin:..." so those become instant no-ops at runtime.
#
# Gated to workflow-security-audit — adds zero cost to every other skill run.
# Best-effort throughout: a failed install is logged, never fatal; the skill degrades
# per-tool and records tool=fail rather than aborting.
set -uo pipefail

SKILL="${1:-}"

# Only relevant to workflow-security-audit; no-op for every other skill.
case "$SKILL" in
  workflow-security-audit) ;;
  *) exit 0 ;;
esac

echo "prefetch-workflow-security-audit: seeding scanner binaries for '$SKILL'"
mkdir -p .audit-bin
export PATH="$PWD/.audit-bin:$HOME/.local/bin:$PATH"

# Must match ZIZMOR_VERSION in skills/workflow-security-audit/SKILL.md step 0b.
ZIZMOR_VERSION="1.25.2"

# --- zizmor (pip install; falls back to pipx) ---
if ! command -v zizmor >/dev/null 2>&1; then
  python3 -m pip install --quiet "zizmor==${ZIZMOR_VERSION}" 2>/dev/null \
    || pipx install "zizmor==${ZIZMOR_VERSION}" 2>/dev/null \
    && echo "  zizmor: installed" \
    || echo "  zizmor: install failed (skill will record zizmor=fail)"
else
  echo "  zizmor: already present ($(command -v zizmor))"
fi

# --- actionlint (release binary → .audit-bin/) ---
if ! command -v actionlint >/dev/null 2>&1; then
  bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash) 2>/dev/null \
    && mv actionlint .audit-bin/ 2>/dev/null \
    && echo "  actionlint: installed (.audit-bin/actionlint)" \
    || echo "  actionlint: install failed (skill will record actionlint=fail)"
else
  echo "  actionlint: already present ($(command -v actionlint))"
fi

echo "prefetch-workflow-security-audit: done (best-effort; skill degrades per-tool)"
exit 0
