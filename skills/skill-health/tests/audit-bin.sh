#!/usr/bin/env bash
# audit-bin.sh — Validate the pre-downloaded audit scanner binaries in .audit-bin/
#
# These binaries (actionlint, zizmor) are committed to avoid network-dependent
# bootstrap inside the Claude sandbox. This test ensures they remain intact,
# executable, and wired to the right architecture before a skill run relies on them.
#
# Usage:
#   ./skills/skill-health/tests/audit-bin.sh
#
# Exit codes:
#   0 = all checks passed
#   1 = one or more checks failed

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AUDIT_BIN="$REPO_ROOT/.audit-bin"

# Colors (disabled in CI)
if [[ -t 1 ]] && [[ "${CI:-false}" != "true" ]]; then
  RED='\033[0;31m'; GREEN='\033[0;32m'; BOLD='\033[1m'; NC='\033[0m'
else
  RED=''; GREEN=''; BOLD=''; NC=''
fi

FAIL_COUNT=0

pass() { echo -e "  ${GREEN}PASS${NC} $1"; }
fail() { echo -e "  ${RED}FAIL${NC} $1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }

echo -e "${BOLD}Audit Binary Validation${NC}"
echo "========================"
echo ""

# --- actionlint binary ---
echo -e "${BOLD}actionlint${NC}"

ACTIONLINT="$AUDIT_BIN/actionlint"
if [[ -f "$ACTIONLINT" ]]; then
  pass "binary exists: .audit-bin/actionlint"
else
  fail "binary missing: .audit-bin/actionlint"
fi

if [[ -x "$ACTIONLINT" ]]; then
  pass "binary is executable"
else
  fail "binary is not executable — run: chmod +x .audit-bin/actionlint"
fi

# Statically linked Go binary — safe to invoke without shared-lib concerns
if [[ -x "$ACTIONLINT" ]]; then
  VERSION_OUTPUT=$("$ACTIONLINT" --version 2>&1 || true)
  if [[ -n "$VERSION_OUTPUT" ]]; then
    pass "--version responds: $VERSION_OUTPUT"
  else
    fail "--version produced no output (binary may be corrupt or wrong arch)"
  fi
fi

echo ""

# --- actionlint.tar.gz archive ---
echo -e "${BOLD}actionlint.tar.gz${NC}"

ARCHIVE="$AUDIT_BIN/actionlint.tar.gz"
if [[ -f "$ARCHIVE" ]]; then
  pass "archive exists: .audit-bin/actionlint.tar.gz"
else
  fail "archive missing: .audit-bin/actionlint.tar.gz"
fi

if [[ -f "$ARCHIVE" ]]; then
  if gzip -t "$ARCHIVE" 2>/dev/null; then
    pass "archive passes gzip integrity check"
  else
    fail "archive is corrupt (gzip -t failed)"
  fi
fi

if [[ -f "$ARCHIVE" ]]; then
  if tar tf "$ARCHIVE" 2>/dev/null | grep -q "actionlint"; then
    pass "archive contains an 'actionlint' entry"
  else
    fail "archive does not contain an 'actionlint' entry — contents: $(tar tf "$ARCHIVE" 2>/dev/null | head -5 || echo '(unreadable)')"
  fi
fi

echo ""

# --- zizmor binary ---
echo -e "${BOLD}zizmor${NC}"

ZIZMOR="$AUDIT_BIN/zizmor"
if [[ -f "$ZIZMOR" ]]; then
  pass "binary exists: .audit-bin/zizmor"
else
  fail "binary missing: .audit-bin/zizmor"
fi

if [[ -x "$ZIZMOR" ]]; then
  pass "binary is executable"
else
  fail "binary is not executable — run: chmod +x .audit-bin/zizmor"
fi

# Verify it is an ELF binary (not a truncated download or wrong filetype)
if [[ -f "$ZIZMOR" ]]; then
  MAGIC=$(head -c 4 "$ZIZMOR" | od -An -tx1 | tr -d ' \n' 2>/dev/null || true)
  if [[ "$MAGIC" == "7f454c46" ]]; then
    pass "binary has ELF magic bytes"
  else
    fail "binary does not start with ELF magic (got: $MAGIC) — may be a corrupt download"
  fi
fi

echo ""
echo "========================"

if [[ $FAIL_COUNT -gt 0 ]]; then
  echo -e "${RED}FAILED — $FAIL_COUNT check(s) did not pass.${NC}"
  exit 1
fi

echo -e "${GREEN}All audit-bin checks passed.${NC}"
exit 0
