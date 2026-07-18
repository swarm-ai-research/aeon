#!/usr/bin/env bash
# audit-bin.test.sh — verify the committed audit scanner binaries are properly
# set up and consistent with the version pin in SKILL.md.
#
# Run:  bash skills/workflow-security-audit/tests/audit-bin.test.sh
# Exit: 0 = all checks passed, 1 = one or more checks failed

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AUDIT_BIN="$REPO_ROOT/.audit-bin"
SKILL_FILE="$REPO_ROOT/skills/workflow-security-audit/SKILL.md"

FAIL_COUNT=0
pass() { echo "  PASS $*"; }
fail() { echo "  FAIL $*" >&2; FAIL_COUNT=$((FAIL_COUNT + 1)); }

echo "Audit-bin tests"
echo "==============="

# 1. Each binary must exist and be executable.
#    SKILL.md step 0b uses [ -x ".audit-bin/<bin>" ] as the primary detection
#    path; a non-executable file silently falls through to network install.
for bin in zizmor actionlint; do
  if [ -x "$AUDIT_BIN/$bin" ]; then
    pass "$bin: exists and is executable"
  elif [ -f "$AUDIT_BIN/$bin" ]; then
    fail "$bin: present but NOT executable — preflight will fall back to network install"
  else
    fail "$bin: missing from .audit-bin/"
  fi
done

# 2. actionlint.tar.gz must pass gzip integrity check (not silently corrupt).
if [ -f "$AUDIT_BIN/actionlint.tar.gz" ]; then
  if gzip -t "$AUDIT_BIN/actionlint.tar.gz" 2>/dev/null; then
    pass "actionlint.tar.gz: passes gzip integrity check"
  else
    fail "actionlint.tar.gz: corrupt (gzip -t failed)"
  fi
else
  fail "actionlint.tar.gz: missing from .audit-bin/"
fi

# 3. actionlint.tar.gz must contain an actionlint entry.
if [ -f "$AUDIT_BIN/actionlint.tar.gz" ]; then
  if tar tzf "$AUDIT_BIN/actionlint.tar.gz" 2>/dev/null | grep -q "actionlint"; then
    pass "actionlint.tar.gz: contains actionlint entry"
  else
    fail "actionlint.tar.gz: does not contain an actionlint entry"
  fi
fi

# 4. zizmor binary version must match ZIZMOR_VERSION pin in SKILL.md.
#    Drift here means the cached binary and the skill's fallback pip install
#    resolve to different versions, producing inconsistent scan results.
PINNED=$(grep -oE 'ZIZMOR_VERSION="[0-9]+\.[0-9]+\.[0-9]+"' "$SKILL_FILE" 2>/dev/null \
         | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)
if [ -z "$PINNED" ]; then
  fail "could not extract ZIZMOR_VERSION from SKILL.md"
elif [ -x "$AUDIT_BIN/zizmor" ]; then
  ACTUAL=$("$AUDIT_BIN/zizmor" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
  if [ "$ACTUAL" = "$PINNED" ]; then
    pass "zizmor: binary version $ACTUAL matches SKILL.md pin"
  else
    fail "zizmor: version mismatch — binary=$ACTUAL, SKILL.md pin=$PINNED (update .audit-bin/ when bumping the pin)"
  fi
fi

# 5. actionlint binary must report a non-empty version string.
if [ -x "$AUDIT_BIN/actionlint" ]; then
  AVERSION=$("$AUDIT_BIN/actionlint" --version 2>&1 | head -1 || true)
  if [ -n "$AVERSION" ]; then
    pass "actionlint: reports version ($AVERSION)"
  else
    fail "actionlint: --version returned empty output"
  fi
fi

# 6. PATH-prepend strategy must make both tools discoverable.
#    This is the mechanism SKILL.md step 0b uses after finding the -x binaries.
SAVED_PATH="$PATH"
export PATH="$AUDIT_BIN:$PATH"
MISSING=""
for bin in zizmor actionlint; do
  command -v "$bin" >/dev/null 2>&1 || MISSING="$MISSING $bin"
done
export PATH="$SAVED_PATH"
if [ -z "$MISSING" ]; then
  pass "PATH bootstrap: both tools found after prepending .audit-bin"
else
  fail "PATH bootstrap: not found after prepending .audit-bin:$MISSING"
fi

echo "==============="
if [ "$FAIL_COUNT" -gt 0 ]; then
  echo "FAILED — $FAIL_COUNT check(s) failed."
  exit 1
fi
echo "All audit-bin tests passed."
