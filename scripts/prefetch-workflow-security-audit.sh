#!/usr/bin/env bash
# Seed actionlint and zizmor onto PATH OUTSIDE the Claude sandbox.
#
# workflow-security-audit bootstraps both scanners at runtime (SKILL.md §0b),
# but the sandbox blocks curl-pipe installers and pip/pipx installs
# (see memory/notes/sandbox-blocks-piped-curl-installers.md). Binaries are
# pre-downloaded into .audit-bin/ by the skill's maintenance pass; this script
# copies them to /tmp/bin/ so the skill's `command -v` checks succeed and the
# in-sandbox install attempts become fast no-ops.
#
# Gated to workflow-security-audit so it adds zero cost to every other run.
set -euo pipefail

SKILL="${1:-}"

case "$SKILL" in
  workflow-security-audit) ;;
  *) exit 0 ;;
esac

AUDIT_BIN="$(cd "$(dirname "$0")/.." && pwd)/.audit-bin"

if [ ! -d "$AUDIT_BIN" ]; then
  echo "prefetch-workflow-security-audit: .audit-bin/ not found, skipping (skill will attempt runtime install)"
  exit 0
fi

mkdir -p /tmp/bin

for tool in actionlint zizmor; do
  src="${AUDIT_BIN}/${tool}"
  if [ -x "$src" ]; then
    cp "$src" "/tmp/bin/${tool}"
    chmod +x "/tmp/bin/${tool}"
    echo "prefetch-workflow-security-audit: seeded ${tool} -> /tmp/bin/${tool}"
  else
    echo "prefetch-workflow-security-audit: ${tool} not found in .audit-bin/ (skill will attempt runtime install)"
  fi
done

# Persist /tmp/bin on PATH for subsequent workflow steps (including Claude).
# Each prefetch runs in its own shell so `export PATH` won't carry over;
# writing to GITHUB_PATH is the GHA-native way to add a dir for all later steps.
if [ -n "${GITHUB_PATH:-}" ]; then
  echo "/tmp/bin" >> "$GITHUB_PATH"
  echo "prefetch-workflow-security-audit: added /tmp/bin to GITHUB_PATH"
fi

echo "prefetch-workflow-security-audit: done"
exit 0
