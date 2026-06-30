#!/usr/bin/env bash
# audit-tools.sh — Verify .audit-bin tools are present, executable, and functional
#
# Usage:
#   ./skills/workflow-security-audit/tests/audit-tools.sh
#
# Exit codes:
#   0 = all checks passed
#   1 = one or more checks failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AUDIT_BIN="$REPO_ROOT/.audit-bin"

# Version pinned in SKILL.md — update here when bumping there
EXPECTED_ZIZMOR_VERSION="1.25.2"

FAIL_COUNT=0
PASS_COUNT=0

pass() { echo "  PASS $1"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { echo "  FAIL $1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }

echo "Audit-tools smoke tests"
echo "======================="
echo ""

# ── actionlint ──────────────────────────────────────────────────────────────

echo "actionlint"

if [[ -f "$AUDIT_BIN/actionlint" ]]; then
  pass "binary present at .audit-bin/actionlint"
else
  fail "binary missing: .audit-bin/actionlint"
fi

if [[ -x "$AUDIT_BIN/actionlint" ]]; then
  pass "binary is executable"
else
  fail "binary is not executable (chmod +x .audit-bin/actionlint)"
fi

if [[ -f "$AUDIT_BIN/actionlint" && -x "$AUDIT_BIN/actionlint" ]]; then
  version_out=$("$AUDIT_BIN/actionlint" --version 2>&1 || true)
  if [[ -n "$version_out" ]]; then
    pass "runs and emits version: $version_out"
  else
    fail "--version produced no output"
  fi
fi

echo ""

# ── actionlint.tar.gz ────────────────────────────────────────────────────────

echo "actionlint.tar.gz"

if [[ -f "$AUDIT_BIN/actionlint.tar.gz" ]]; then
  pass "archive present at .audit-bin/actionlint.tar.gz"
else
  fail "archive missing: .audit-bin/actionlint.tar.gz"
fi

if [[ -f "$AUDIT_BIN/actionlint.tar.gz" ]]; then
  archive_size=$(wc -c < "$AUDIT_BIN/actionlint.tar.gz")
  if [[ "$archive_size" -gt 0 ]]; then
    pass "archive is non-empty ($archive_size bytes)"
  else
    fail "archive is empty (0 bytes) — likely corrupted"
  fi
fi

if command -v tar >/dev/null 2>&1 && [[ -f "$AUDIT_BIN/actionlint.tar.gz" ]]; then
  if tar -tzf "$AUDIT_BIN/actionlint.tar.gz" >/dev/null 2>&1; then
    pass "archive is a valid gzip tarball"
  else
    fail "archive is not a valid gzip tarball — corrupted or wrong format"
  fi
fi

echo ""

# ── zizmor ───────────────────────────────────────────────────────────────────

echo "zizmor"

if [[ -f "$AUDIT_BIN/zizmor" ]]; then
  pass "binary present at .audit-bin/zizmor"
else
  fail "binary missing: .audit-bin/zizmor"
fi

if [[ -x "$AUDIT_BIN/zizmor" ]]; then
  pass "binary is executable"
else
  fail "binary is not executable (chmod +x .audit-bin/zizmor)"
fi

if [[ -f "$AUDIT_BIN/zizmor" && -x "$AUDIT_BIN/zizmor" ]]; then
  version_out=$("$AUDIT_BIN/zizmor" --version 2>&1 || true)
  if [[ -n "$version_out" ]]; then
    pass "runs and emits version: $version_out"
  else
    fail "--version produced no output"
  fi

  # Version must match the pin in SKILL.md so drift is caught before a run
  if echo "$version_out" | grep -qF "$EXPECTED_ZIZMOR_VERSION"; then
    pass "version matches SKILL.md pin ($EXPECTED_ZIZMOR_VERSION)"
  else
    fail "version mismatch — SKILL.md pins $EXPECTED_ZIZMOR_VERSION but binary reports: $version_out"
  fi
fi

echo ""

# ── Summary ──────────────────────────────────────────────────────────────────

echo "======================="
echo "  Pass: $PASS_COUNT"
if [[ $FAIL_COUNT -gt 0 ]]; then
  echo "  Fail: $FAIL_COUNT"
  echo ""
  echo "Audit-tools smoke tests FAILED."
  exit 1
fi
echo ""
echo "All audit-tools smoke tests passed."
exit 0
