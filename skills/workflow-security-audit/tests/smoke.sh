#!/usr/bin/env bash
# smoke.sh — Validate .audit-bin/ pre-cached binaries for workflow-security-audit
#
# The SKILL.md preflight (step 0b) gates on [ -x ".audit-bin/zizmor" ] and
# [ -x ".audit-bin/actionlint" ] to skip network installs on CI runners.
# These tests cover the uncovered branches:
#   1. Executable bit set (condition the SKILL relies on)
#   2. tar.gz integrity (archive never verified elsewhere)
#   3. Version pins in SKILL.md match the committed binaries
#
# Run from the repo root:
#   ./skills/workflow-security-audit/tests/smoke.sh
#
# Exit codes:
#   0 = all checks passed
#   1 = one or more checks failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AUDIT_BIN="${REPO_ROOT}/.audit-bin"

# Keep in sync with ZIZMOR_VERSION in SKILL.md
EXPECTED_ZIZMOR_VERSION="1.25.2"
# From memory/logs/2026-07-05.md "actionlint=ok (1.7.12)"
EXPECTED_ACTIONLINT_VERSION="1.7.12"

FAIL_COUNT=0
PASS_COUNT=0

pass() { echo "  PASS $1"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { echo "  FAIL $1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }

echo "audit-bin smoke tests"
echo "====================="
echo ""

# 1. actionlint binary exists
if [ -f "${AUDIT_BIN}/actionlint" ]; then
  pass "actionlint binary present"
else
  fail "actionlint binary missing at .audit-bin/actionlint"
fi

# 2. actionlint is executable — SKILL.md step 0b: if [ -x ".audit-bin/actionlint" ]
#    If this bit is missing the SKILL falls through to a curl-based network install
#    which fails silently in the GHA sandbox, leaving actionlint unavailable.
if [ -x "${AUDIT_BIN}/actionlint" ]; then
  pass "actionlint is executable"
else
  fail "actionlint is NOT executable — SKILL.md preflight will miss the binary and fall back to network install"
fi

# 3. zizmor binary exists
if [ -f "${AUDIT_BIN}/zizmor" ]; then
  pass "zizmor binary present"
else
  fail "zizmor binary missing at .audit-bin/zizmor"
fi

# 4. zizmor is executable — same branch as above for zizmor
if [ -x "${AUDIT_BIN}/zizmor" ]; then
  pass "zizmor is executable"
else
  fail "zizmor is NOT executable — SKILL.md preflight will miss the binary and fall back to pipx/pip"
fi

# 5. actionlint.tar.gz exists (backup archive for re-extraction)
if [ -f "${AUDIT_BIN}/actionlint.tar.gz" ]; then
  pass "actionlint.tar.gz present"
else
  fail "actionlint.tar.gz missing at .audit-bin/actionlint.tar.gz"
fi

# 6. actionlint.tar.gz is a valid gzip archive — catches corruption/truncation
#    that wouldn't surface until someone tries to re-extract the binary.
if gzip -t "${AUDIT_BIN}/actionlint.tar.gz" 2>/dev/null; then
  pass "actionlint.tar.gz passes gzip integrity check"
else
  fail "actionlint.tar.gz is corrupt or not a valid gzip archive"
fi

# 7. actionlint.tar.gz contains an actionlint entry — not an empty or wrong archive
if tar -tzf "${AUDIT_BIN}/actionlint.tar.gz" 2>/dev/null | grep -q "actionlint"; then
  pass "actionlint.tar.gz contains an actionlint binary entry"
else
  fail "actionlint.tar.gz has no actionlint entry — wrong archive committed"
fi

# 8. actionlint version matches SKILL.md-documented pin
AL_VERSION=$("${AUDIT_BIN}/actionlint" -version 2>/dev/null || true)
if echo "${AL_VERSION}" | grep -qF "${EXPECTED_ACTIONLINT_VERSION}"; then
  pass "actionlint version matches pin (${EXPECTED_ACTIONLINT_VERSION})"
else
  fail "actionlint version mismatch: expected ${EXPECTED_ACTIONLINT_VERSION}, binary reports '${AL_VERSION}' — update documented version or replace the binary"
fi

# 9. zizmor version matches ZIZMOR_VERSION pin in SKILL.md
ZZ_VERSION=$("${AUDIT_BIN}/zizmor" --version 2>/dev/null || true)
if echo "${ZZ_VERSION}" | grep -qF "${EXPECTED_ZIZMOR_VERSION}"; then
  pass "zizmor version matches ZIZMOR_VERSION pin (${EXPECTED_ZIZMOR_VERSION})"
else
  fail "zizmor version mismatch: ZIZMOR_VERSION=${EXPECTED_ZIZMOR_VERSION} but binary reports '${ZZ_VERSION}' — update SKILL.md pin or replace .audit-bin/zizmor"
fi

echo ""
echo "====================="
echo "Pass: ${PASS_COUNT}"
if [ "${FAIL_COUNT}" -gt 0 ]; then
  echo "Fail: ${FAIL_COUNT}"
  echo ""
  echo "audit-bin checks FAILED — one or more binaries are missing, not executable, or version-mismatched."
  exit 1
fi
echo ""
echo "All audit-bin smoke tests passed."
exit 0
