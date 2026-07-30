#!/usr/bin/env bash
# Tests for .audit-bin/ pre-committed scanner binaries.
#
# workflow-security-audit depends on these binaries being present and executable.
# This test catches accidental deletion, permission loss, or partial updates
# (e.g. tarball updated but binary not replaced).
#
# Exit codes: 0 = all passed, 1 = failures
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AUDIT_BIN="$REPO_ROOT/.audit-bin"

PASS=0; FAIL=0

ok()   { echo "  PASS: $1"; PASS=$((PASS+1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

echo "audit-bin tests"
echo "==============="

# actionlint binary
[[ -f "$AUDIT_BIN/actionlint" ]] \
  && ok "actionlint binary exists" \
  || fail "actionlint binary missing from .audit-bin/"

[[ -x "$AUDIT_BIN/actionlint" ]] \
  && ok "actionlint is executable" \
  || fail "actionlint is not executable (chmod +x needed)"

# zizmor binary
[[ -f "$AUDIT_BIN/zizmor" ]] \
  && ok "zizmor binary exists" \
  || fail "zizmor binary missing from .audit-bin/"

[[ -x "$AUDIT_BIN/zizmor" ]] \
  && ok "zizmor is executable" \
  || fail "zizmor is not executable (chmod +x needed)"

# actionlint source tarball (used for version pinning and reproducibility)
[[ -f "$AUDIT_BIN/actionlint.tar.gz" ]] \
  && ok "actionlint.tar.gz exists" \
  || fail "actionlint.tar.gz missing — version cannot be verified"

# Consistency check: tarball should not be newer than the binary
# (a common mistake is updating the tarball but forgetting to rebuild the binary)
if [[ -f "$AUDIT_BIN/actionlint.tar.gz" && -f "$AUDIT_BIN/actionlint" ]]; then
  if [[ "$AUDIT_BIN/actionlint.tar.gz" -nt "$AUDIT_BIN/actionlint" ]]; then
    fail "actionlint.tar.gz is newer than actionlint binary — binary may be stale"
  else
    ok "actionlint binary is not older than its tarball"
  fi
fi

echo ""
echo "==============="
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && echo "PASSED" && exit 0
echo "FAILED"; exit 1
