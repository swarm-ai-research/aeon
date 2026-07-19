#!/usr/bin/env bash
# audit-bin.test.sh — Validate .audit-bin/ pre-cached binaries for workflow-security-audit.
#
# Tests the uncovered branches from SKILL.md step 0b:
#   - both binaries exist and are executable (the [ -x ".audit-bin/..." ] path)
#   - the actionlint archive is a valid gzip (sanity-check the committed tarball)
#   - the zizmor binary reports the version matching ZIZMOR_VERSION in SKILL.md
#     (catches version-pin drift between the committed binary and SKILL.md)
#
# Usage:
#   ./skills/workflow-security-audit/tests/audit-bin.test.sh
#
# Exit codes:
#   0 = all checks passed
#   1 = one or more checks failed

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AUDIT_BIN="$REPO_ROOT/.audit-bin"
SKILL_MD="$REPO_ROOT/skills/workflow-security-audit/SKILL.md"

PASS=0
FAIL=0

pass() { echo "  PASS $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL $1" >&2; FAIL=$((FAIL + 1)); }

echo "audit-bin integrity checks"
echo "=========================="
echo ""

# --- 1. zizmor binary is present and executable --------------------------------
# Mirrors the `[ -x ".audit-bin/zizmor" ]` branch in SKILL.md step 0b.
echo "1. zizmor executable"
if [[ -f "$AUDIT_BIN/zizmor" ]]; then
  pass "zizmor file exists"
else
  fail "zizmor missing from .audit-bin/"
fi

if [[ -x "$AUDIT_BIN/zizmor" ]]; then
  pass "zizmor is executable"
else
  fail "zizmor is not executable (chmod +x needed)"
fi

# --- 2. actionlint binary is present and executable ----------------------------
# Mirrors the `[ -x ".audit-bin/actionlint" ]` branch in SKILL.md step 0b.
echo ""
echo "2. actionlint executable"
if [[ -f "$AUDIT_BIN/actionlint" ]]; then
  pass "actionlint file exists"
else
  fail "actionlint missing from .audit-bin/"
fi

if [[ -x "$AUDIT_BIN/actionlint" ]]; then
  pass "actionlint is executable"
else
  fail "actionlint is not executable (chmod +x needed)"
fi

# --- 3. actionlint.tar.gz is a valid gzip archive ------------------------------
# Catches a corrupt or truncated tarball commit (the tarball is kept alongside
# the binary so operators can verify provenance; it must be a readable archive).
echo ""
echo "3. actionlint.tar.gz archive integrity"
TARBALL="$AUDIT_BIN/actionlint.tar.gz"
if [[ -f "$TARBALL" ]]; then
  pass "actionlint.tar.gz exists"
  if gunzip -t "$TARBALL" 2>/dev/null; then
    pass "actionlint.tar.gz is a valid gzip"
  else
    fail "actionlint.tar.gz failed gunzip -t (corrupt archive)"
  fi
else
  fail "actionlint.tar.gz missing from .audit-bin/"
fi

# --- 4. zizmor version matches the pin in SKILL.md ----------------------------
# SKILL.md pins ZIZMOR_VERSION="1.25.2". If the committed binary is upgraded
# without bumping the pin (or vice-versa), network installs would download a
# different version than what's in the repo, causing audit drift.
echo ""
echo "4. zizmor version pin consistency"
if [[ ! -f "$SKILL_MD" ]]; then
  fail "SKILL.md not found — cannot verify version pin"
else
  PINNED=$(grep 'ZIZMOR_VERSION=' "$SKILL_MD" | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
  if [[ -z "$PINNED" ]]; then
    fail "could not extract ZIZMOR_VERSION from SKILL.md"
  else
    pass "SKILL.md pins zizmor to $PINNED"

    if [[ -x "$AUDIT_BIN/zizmor" ]]; then
      # zizmor --version outputs e.g. "zizmor 1.25.2"
      BINARY_VER=$("$AUDIT_BIN/zizmor" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
      if [[ -z "$BINARY_VER" ]]; then
        fail "could not parse version from \`zizmor --version\` output"
      elif [[ "$BINARY_VER" == "$PINNED" ]]; then
        pass "binary version ($BINARY_VER) matches SKILL.md pin"
      else
        fail "version mismatch: binary=$BINARY_VER SKILL.md=$PINNED — update one to match"
      fi
    else
      fail "skipping version check — zizmor binary is not executable"
    fi
  fi
fi

# --- Summary -------------------------------------------------------------------
echo ""
echo "=========================="
echo "$PASS passed, $FAIL failed"
echo ""
if [[ $FAIL -gt 0 ]]; then
  echo "FAILED: $FAIL check(s) need attention." >&2
  exit 1
fi
echo "All checks passed."
exit 0
