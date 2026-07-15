#!/usr/bin/env bash
# test_audit_bins.sh — Smoke tests for the cached audit binaries in .audit-bin/
#
# Verifies that .audit-bin/actionlint and .audit-bin/zizmor are present,
# executable, and respond correctly, and that the actionlint tarball is a
# valid gzip archive containing the binary.
#
# Usage:  ./skills/workflow-security-audit/tests/test_audit_bins.sh
# Exit:   0 = all checks passed, 1 = one or more failed

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
BIN_DIR="${REPO_ROOT}/.audit-bin"

PASS=0
FAIL=0

pass() { echo "  PASS  $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }

echo "=== Audit-bin smoke tests ==="
echo ""

# 1. Binaries exist
if [[ -f "${BIN_DIR}/actionlint" ]]; then
    pass "actionlint binary present"
else
    fail "actionlint binary missing from ${BIN_DIR}"
fi

if [[ -f "${BIN_DIR}/zizmor" ]]; then
    pass "zizmor binary present"
else
    fail "zizmor binary missing from ${BIN_DIR}"
fi

if [[ -f "${BIN_DIR}/actionlint.tar.gz" ]]; then
    pass "actionlint.tar.gz present"
else
    fail "actionlint.tar.gz missing from ${BIN_DIR}"
fi

# 2. Binaries are executable
if [[ -x "${BIN_DIR}/actionlint" ]]; then
    pass "actionlint is executable"
else
    fail "actionlint is not executable (missing +x bit)"
fi

if [[ -x "${BIN_DIR}/zizmor" ]]; then
    pass "zizmor is executable"
else
    fail "zizmor is not executable (missing +x bit)"
fi

# 3. Tarball is valid gzip and contains the actionlint binary
if gzip -t "${BIN_DIR}/actionlint.tar.gz" 2>/dev/null; then
    pass "actionlint.tar.gz passes gzip integrity check"
else
    fail "actionlint.tar.gz is corrupt (gzip -t failed)"
fi

if tar -tzf "${BIN_DIR}/actionlint.tar.gz" 2>/dev/null | grep -q "actionlint"; then
    pass "actionlint.tar.gz contains an 'actionlint' entry"
else
    fail "actionlint.tar.gz does not contain expected 'actionlint' entry"
fi

# 4. Binaries respond to --version / --help without crashing
if ACTIONLINT_OUT=$("${BIN_DIR}/actionlint" --version 2>&1 || true); then
    if echo "$ACTIONLINT_OUT" | grep -qE '[0-9]+\.[0-9]+'; then
        pass "actionlint --version returns a version string"
    else
        fail "actionlint --version output did not contain a version number: ${ACTIONLINT_OUT}"
    fi
else
    fail "actionlint --version exited with error"
fi

if ZIZMOR_OUT=$("${BIN_DIR}/zizmor" --version 2>&1 || true); then
    if echo "$ZIZMOR_OUT" | grep -qE '[0-9]+\.[0-9]+'; then
        pass "zizmor --version returns a version string"
    else
        fail "zizmor --version output did not contain a version number: ${ZIZMOR_OUT}"
    fi
else
    fail "zizmor --version exited with error"
fi

# 5. Binaries are non-empty (guard against a zero-byte commit accident)
ACTIONLINT_SIZE=$(stat -c%s "${BIN_DIR}/actionlint" 2>/dev/null || stat -f%z "${BIN_DIR}/actionlint" 2>/dev/null || echo 0)
if [[ "$ACTIONLINT_SIZE" -gt 1000000 ]]; then
    pass "actionlint binary size looks reasonable (${ACTIONLINT_SIZE} bytes)"
else
    fail "actionlint binary is suspiciously small: ${ACTIONLINT_SIZE} bytes"
fi

ZIZMOR_SIZE=$(stat -c%s "${BIN_DIR}/zizmor" 2>/dev/null || stat -f%z "${BIN_DIR}/zizmor" 2>/dev/null || echo 0)
if [[ "$ZIZMOR_SIZE" -gt 1000000 ]]; then
    pass "zizmor binary size looks reasonable (${ZIZMOR_SIZE} bytes)"
else
    fail "zizmor binary is suspiciously small: ${ZIZMOR_SIZE} bytes"
fi

echo ""
echo "=== Results: ${PASS} passed, ${FAIL} failed ==="

if [[ $FAIL -gt 0 ]]; then
    exit 1
fi
exit 0
