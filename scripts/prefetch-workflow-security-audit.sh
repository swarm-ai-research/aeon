#!/usr/bin/env bash
# Pre-install workflow-security-audit scanner binaries OUTSIDE the Claude sandbox.
#
# The GitHub Actions sandbox blocks `bash <(curl …)` and `pipx install` at
# runtime (observed 2026-06-21: both zizmor and actionlint installs failed,
# leaving the skill degraded to hand-rolled regex only). This script runs in
# the workflow's prefetch phase (before Claude starts, with full network
# access), seeding the committed binaries from .audit-bin/ into /tmp/bin so
# the skill's `command -v` checks succeed inside the sandbox.
#
# Falls back to live downloads if .audit-bin/ binaries are absent or stale.
# Best-effort throughout — a failed install is non-fatal; the skill degrades
# per-tool and marks the run as WORKFLOW_AUDIT_TOOL_DEGRADED.
set -uo pipefail

SKILL="${1:-}"

# Only relevant to workflow-security-audit; no-op for every other skill.
case "$SKILL" in
  workflow-security-audit) ;;
  *) exit 0 ;;
esac

echo "prefetch-workflow-security-audit: seeding scanner binaries for '$SKILL'"
mkdir -p /tmp/bin
echo "/tmp/bin" >> "${GITHUB_PATH:-/dev/null}"

REPO_BIN="$(cd "$(dirname "$0")/.." && pwd)/.audit-bin"

# --- zizmor (Trail of Bits, SARIF-capable GH Actions auditor) ---
if [ -x "$REPO_BIN/zizmor" ]; then
  cp "$REPO_BIN/zizmor" /tmp/bin/zizmor
  chmod +x /tmp/bin/zizmor
  echo "  zizmor: installed from .audit-bin/ ($(/tmp/bin/zizmor --version 2>&1 | head -1))"
else
  echo "  zizmor: .audit-bin/zizmor absent, trying pipx/pip..."
  ZIZMOR_VERSION="1.25.2"
  pipx install "zizmor==${ZIZMOR_VERSION}" 2>/dev/null \
    || python3 -m pip install --user "zizmor==${ZIZMOR_VERSION}" 2>/dev/null \
    || echo "  zizmor: install failed (skill will record zizmor=fail)"
fi

# --- actionlint (Rhymond's syntax-level workflow linter) ---
if [ -x "$REPO_BIN/actionlint" ]; then
  cp "$REPO_BIN/actionlint" /tmp/bin/actionlint
  chmod +x /tmp/bin/actionlint
  echo "  actionlint: installed from .audit-bin/ ($(/tmp/bin/actionlint --version 2>&1 | head -1))"
else
  echo "  actionlint: .audit-bin/actionlint absent, trying curl installer..."
  curl -sSfL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash \
    | bash -s -- -b /tmp/bin 2>/dev/null \
    || echo "  actionlint: install failed (skill will record actionlint=fail)"
fi

echo "prefetch-workflow-security-audit: done"
exit 0
