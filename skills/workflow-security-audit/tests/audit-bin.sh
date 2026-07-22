#!/usr/bin/env bash
# audit-bin.sh — Validate the pre-committed scanner binaries in .audit-bin/
#
# Tests that the committed binaries are present, executable, and well-formed.
# Run from repo root: ./skills/workflow-security-audit/tests/audit-bin.sh
#
# Exit codes:
#   0 = all checks passed
#   1 = one or more checks failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AUDIT_BIN="$REPO_ROOT/.audit-bin"

PASS=0
FAIL=0

pass() { echo "  PASS $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL $1"; FAIL=$((FAIL + 1)); }

echo "audit-bin sanity checks"
echo "======================="
echo ""

# --- actionlint ---

echo "actionlint"

if [[ -f "$AUDIT_BIN/actionlint" ]]; then
  pass "file exists"
else
  fail "file missing: $AUDIT_BIN/actionlint"
fi

if [[ -x "$AUDIT_BIN/actionlint" ]]; then
  pass "executable bit set"
else
  fail "not executable — skill will fail to run it"
fi

if [[ -s "$AUDIT_BIN/actionlint" ]]; then
  pass "non-zero size"
else
  fail "file is empty"
fi

# Verify ELF magic bytes (first 4 bytes: 0x7f 0x45 0x4c 0x46)
magic=$(od -A n -N 4 -t x1 "$AUDIT_BIN/actionlint" 2>/dev/null | tr -d ' \n' || true)
if [[ "$magic" == "7f454c46" ]]; then
  pass "ELF magic bytes valid"
else
  fail "unexpected magic bytes '$magic' — binary may be corrupt or wrong format"
fi

echo ""

# --- actionlint.tar.gz ---

echo "actionlint.tar.gz"

if [[ -f "$AUDIT_BIN/actionlint.tar.gz" ]]; then
  pass "file exists"
else
  fail "file missing: $AUDIT_BIN/actionlint.tar.gz"
fi

if [[ -s "$AUDIT_BIN/actionlint.tar.gz" ]]; then
  pass "non-zero size"
else
  fail "file is empty"
fi

# Verify gzip magic bytes (first 2 bytes: 0x1f 0x8b)
gz_magic=$(od -A n -N 2 -t x1 "$AUDIT_BIN/actionlint.tar.gz" 2>/dev/null | tr -d ' \n' || true)
if [[ "$gz_magic" == "1f8b" ]]; then
  pass "gzip magic bytes valid"
else
  fail "unexpected magic bytes '$gz_magic' — archive may be corrupt"
fi

echo ""

# --- zizmor ---

echo "zizmor"

if [[ -f "$AUDIT_BIN/zizmor" ]]; then
  pass "file exists"
else
  fail "file missing: $AUDIT_BIN/zizmor"
fi

if [[ -x "$AUDIT_BIN/zizmor" ]]; then
  pass "executable bit set"
else
  fail "not executable — skill will fail to run it"
fi

if [[ -s "$AUDIT_BIN/zizmor" ]]; then
  pass "non-zero size"
else
  fail "file is empty"
fi

zizmor_magic=$(od -A n -N 4 -t x1 "$AUDIT_BIN/zizmor" 2>/dev/null | tr -d ' \n' || true)
if [[ "$zizmor_magic" == "7f454c46" ]]; then
  pass "ELF magic bytes valid"
else
  fail "unexpected magic bytes '$zizmor_magic' — binary may be corrupt or wrong format"
fi

# Confirm both binaries are x86-64 (EI_CLASS=2 byte 4, EI_DATA=1 byte 5, e_machine=0x3e bytes 18-19)
# Byte index 18 (0-indexed) = 0x3e (62) for x86-64
al_machine=$(od -A n -j 18 -N 2 -t x1 "$AUDIT_BIN/actionlint" 2>/dev/null | tr -d ' \n' || true)
ziz_machine=$(od -A n -j 18 -N 2 -t x1 "$AUDIT_BIN/zizmor" 2>/dev/null | tr -d ' \n' || true)
if [[ "$al_machine" == "3e00" ]]; then
  pass "actionlint is x86-64"
else
  fail "actionlint e_machine=$al_machine — expected 3e00 (x86-64)"
fi
if [[ "$ziz_machine" == "3e00" ]]; then
  pass "zizmor is x86-64"
else
  fail "zizmor e_machine=$ziz_machine — expected 3e00 (x86-64)"
fi

echo ""

# --- version execution (skip if not running on x86-64 Linux) ---

arch=$(uname -m 2>/dev/null || true)
os=$(uname -s 2>/dev/null || true)

if [[ "$os" == "Linux" && "$arch" == "x86_64" ]]; then
  echo "version checks (Linux x86_64)"

  al_ver=$("$AUDIT_BIN/actionlint" --version 2>&1 || true)
  if echo "$al_ver" | grep -qE '[0-9]+\.[0-9]+\.[0-9]+'; then
    pass "actionlint --version: $al_ver"
  else
    fail "actionlint --version produced no semver output: $al_ver"
  fi

  ziz_ver=$("$AUDIT_BIN/zizmor" --version 2>&1 || true)
  if echo "$ziz_ver" | grep -qE '[0-9]+\.[0-9]+\.[0-9]+'; then
    pass "zizmor --version: $ziz_ver"
  else
    fail "zizmor --version produced no semver output: $ziz_ver"
  fi

  echo ""
else
  echo "  SKIP version execution — not on Linux x86_64 (got $os/$arch)"
  echo ""
fi

# --- summary ---

echo "======================="
echo "Pass: $PASS  Fail: $FAIL"
echo ""

if [[ $FAIL -gt 0 ]]; then
  echo "FAILED — $FAIL check(s) did not pass"
  exit 1
fi

echo "All checks passed"
exit 0
