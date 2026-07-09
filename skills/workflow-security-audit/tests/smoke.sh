#!/usr/bin/env bash
# smoke.sh — Verify .audit-bin/ scanner binaries are present, executable, and
# return sensible output.
#
# Run from repo root:  skills/workflow-security-audit/tests/smoke.sh
# Exit 0 = all checks passed, Exit 1 = one or more checks failed.
#
# These tests cover the gap left by the staged binaries in .audit-bin/:
# actionlint and zizmor are pre-fetched so the sandbox-blocked runtime installs
# (pip/curl) can be skipped, but no test previously validated the binaries.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AUDIT_BIN="$REPO_ROOT/.audit-bin"

PASS=0
FAIL=0

pass() { echo "  PASS $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL $1"; FAIL=$((FAIL + 1)); }

echo "Audit-bin Smoke Tests"
echo "====================="
echo ""

# ── actionlint ──────────────────────────────────────────────────────────────

echo "actionlint"

if [[ -f "$AUDIT_BIN/actionlint" ]]; then
  pass "binary present: .audit-bin/actionlint"
else
  fail "binary missing: .audit-bin/actionlint"
fi

if [[ -x "$AUDIT_BIN/actionlint" ]]; then
  pass "binary is executable"
else
  fail "binary is not executable — chmod +x .audit-bin/actionlint required"
fi

if [[ -x "$AUDIT_BIN/actionlint" ]]; then
  # -version prints a bare semver string to stdout (e.g. "1.7.7").
  ver=$("$AUDIT_BIN/actionlint" -version 2>&1 || true)
  if echo "$ver" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
    pass "-version outputs semver: $ver"
  else
    fail "-version did not output a semver string (got: ${ver:0:80})"
  fi
fi

# Edge case: scan a minimal workflow that has no findings — actionlint must
# exit 0 and produce a valid (empty) JSON array, not crash or emit garbage.
if [[ -x "$AUDIT_BIN/actionlint" ]]; then
  TMP=$(mktemp -d)
  cat > "$TMP/minimal.yml" << 'YAML'
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
YAML
  json_out=$("$AUDIT_BIN/actionlint" -format '{{json .}}' "$TMP/minimal.yml" 2>/dev/null || true)
  # Output must be parseable JSON (empty array [] when no findings).
  if printf '%s' "$json_out" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
    pass "-format '{{json .}}' produces valid JSON on a clean workflow"
  else
    fail "-format '{{json .}}' did not produce valid JSON (got: ${json_out:0:120})"
  fi
  rm -rf "$TMP"
fi

echo ""

# ── zizmor ──────────────────────────────────────────────────────────────────

echo "zizmor"

if [[ -f "$AUDIT_BIN/zizmor" ]]; then
  pass "binary present: .audit-bin/zizmor"
else
  fail "binary missing: .audit-bin/zizmor"
fi

if [[ -x "$AUDIT_BIN/zizmor" ]]; then
  pass "binary is executable"
else
  fail "binary is not executable — chmod +x .audit-bin/zizmor required"
fi

if [[ -x "$AUDIT_BIN/zizmor" ]]; then
  # --version prints "zizmor X.Y.Z" to stdout.
  ver=$("$AUDIT_BIN/zizmor" --version 2>&1 || true)
  if echo "$ver" | grep -qE '[0-9]+\.[0-9]+\.[0-9]+'; then
    pass "--version contains semver: $ver"
  else
    fail "--version did not contain a semver string (got: ${ver:0:80})"
  fi
fi

# Edge case: scan a minimal workflow directory — zizmor must not crash and
# must emit a SARIF document (well-formed JSON with a 'runs' key).
if [[ -x "$AUDIT_BIN/zizmor" ]]; then
  TMP=$(mktemp -d)
  WF_DIR="$TMP/.github/workflows"
  mkdir -p "$WF_DIR"
  cat > "$WF_DIR/ci.yml" << 'YAML'
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
YAML
  sarif_out=$("$AUDIT_BIN/zizmor" --format sarif "$WF_DIR" 2>/dev/null || true)
  if printf '%s' "$sarif_out" | python3 -c "import sys, json; d=json.load(sys.stdin); assert 'runs' in d" 2>/dev/null; then
    pass "--format sarif produces a SARIF document with 'runs' key"
  else
    fail "--format sarif did not produce a valid SARIF document (got: ${sarif_out:0:120})"
  fi
  rm -rf "$TMP"
fi

echo ""

# ── Summary ─────────────────────────────────────────────────────────────────

echo "====================="
printf "Pass: %d  Fail: %d\n" "$PASS" "$FAIL"
echo ""

if [[ $FAIL -gt 0 ]]; then
  echo "Audit-bin smoke tests FAILED."
  exit 1
fi
echo "All audit-bin smoke tests passed."
exit 0
