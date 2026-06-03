#!/usr/bin/env bash
# Pre-install vuln-scanner's scanner binaries OUTSIDE the Claude sandbox.
#
# vuln-scanner shells out to four scanners (semgrep, trufflehog, osv-scanner,
# slither). Per the skill's Sandbox note, none are pre-installed on the GitHub
# Actions runner, and the in-sandbox `pip install` / `curl | sh` the skill
# attempts at runtime can be blocked — leaving every scanner `fail`, which the
# skill is required to report as an *error* (an all-scanners-fail run must never
# be reported as clean). That burns the Saturday run with no audit.
#
# This script runs in the workflow's prefetch phase (.github/workflows/aeon.yml
# loops scripts/prefetch-*.sh before Claude starts, with full network access),
# so the installs land here. It pre-seeds the exact locations the skill expects:
#   - semgrep            -> on PATH (pip)
#   - /tmp/bin/trufflehog
#   - /tmp/bin/osv-scanner
#   - slither            -> on PATH (pip, slither-analyzer)
# The skill re-attempts each install at runtime with `|| true`; once seeded here
# those become fast no-ops and the binaries resolve inside the sandbox.
#
# Gated to the vuln-scanner skill so it adds zero cost to every other run.
# Best-effort throughout: a missing scanner is logged and skipped, never fatal —
# the skill already degrades per-scanner (records tool=fail, continues).
set -uo pipefail

SKILL="${1:-}"

# Only relevant to vuln-scanner; no-op for every other skill.
case "$SKILL" in
  vuln-scanner) ;;
  *) exit 0 ;;
esac

echo "prefetch-vuln-scanner: seeding scanner binaries for '$SKILL'"
mkdir -p /tmp/bin
export PATH="/tmp/bin:$PATH"

# --- SAST: Semgrep OSS (pip, lands on PATH) ---
pip install --quiet semgrep 2>/dev/null \
  && echo "  semgrep: installed ($(command -v semgrep))" \
  || echo "  semgrep: install failed (skill will record semgrep=fail)"

# --- Secrets: TruffleHog (pinned installer into /tmp/bin) ---
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh \
  | sh -s -- -b /tmp/bin 2>/dev/null \
  && echo "  trufflehog: installed (/tmp/bin/trufflehog)" \
  || echo "  trufflehog: install failed (skill will record trufflehog=fail)"

# --- Dependencies: osv-scanner (release binary into /tmp/bin) ---
if curl -sSfL -o /tmp/bin/osv-scanner \
     https://github.com/google/osv-scanner/releases/latest/download/osv-scanner_linux_amd64 2>/dev/null; then
  chmod +x /tmp/bin/osv-scanner
  echo "  osv-scanner: installed (/tmp/bin/osv-scanner)"
else
  echo "  osv-scanner: install failed (skill will record osv=fail)"
fi

# --- Smart contracts: Slither (pip, only useful for Solidity repos) ---
pip install --quiet slither-analyzer 2>/dev/null \
  && echo "  slither: installed ($(command -v slither))" \
  || echo "  slither: install failed (only relevant to smart-contract repos)"

echo "prefetch-vuln-scanner: done (best-effort; the skill degrades per-scanner)"
exit 0
