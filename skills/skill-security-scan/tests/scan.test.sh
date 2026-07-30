#!/usr/bin/env bash
# Tests for skill-security-scan/scan.sh
#
# Covers uncovered branches: HIGH/MEDIUM/LOW exit codes, JSON output mode,
# and the POSIX-ERE word-boundary edge case for "git push -f" vs "-fast".
#
# Exit codes: 0 = all passed, 1 = failures
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCAN="$SCRIPT_DIR/../scan.sh"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

PASS=0; FAIL=0

ok()   { echo "  PASS: $1"; PASS=$((PASS+1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

skill_file() {
  local name="$1" content="$2"
  mkdir -p "$WORK/$name"
  printf '%s' "$content" > "$WORK/$name/SKILL.md"
  echo "$WORK/$name/SKILL.md"
}

echo "scan.sh tests"
echo "============="

# 1. No arguments → usage error, exit 2
rc=0; bash "$SCAN" >/dev/null 2>&1 || rc=$?
[[ $rc -eq 2 ]] && ok "no args exits 2" || fail "no args: expected 2, got $rc"

# 2. Clean file with no risky patterns → PASS, exit 0
f=$(skill_file clean $'---\nname: safe-skill\ndescription: safe\n---\nJust reads and calls ./notify with a message.\n')
out=$(bash "$SCAN" "$f" 2>&1); rc=$?
[[ $rc -eq 0 ]]       && ok "clean file exits 0"          || fail "clean file: expected 0, got $rc"
echo "$out" | grep -q "PASS" && ok "clean file output contains PASS" || fail "clean file: PASS not in output"

# 3. HIGH pattern (eval) → FAIL, exit 1
f=$(skill_file high $'---\nname: risky\ndescription: risky\n---\nRun: eval $USER_INPUT\n')
out=$(bash "$SCAN" "$f" 2>&1); rc=$?
[[ $rc -eq 1 ]]       && ok "HIGH (eval) exits 1"    || fail "HIGH (eval): expected 1, got $rc"
echo "$out" | grep -q "FAIL" && ok "HIGH output contains FAIL" || fail "HIGH: FAIL not in output"

# 4. MEDIUM-only (git push --force) → WARN, exit 0
#    Exit code must be 0 because only TOTAL_FAIL triggers exit 1
f=$(skill_file medium $'---\nname: medium\ndescription: medium\n---\nRun: git push --force\n')
out=$(bash "$SCAN" "$f" 2>&1); rc=$?
[[ $rc -eq 0 ]]        && ok "MEDIUM-only exits 0"         || fail "MEDIUM-only: expected 0, got $rc"
echo "$out" | grep -q "WARN" && ok "MEDIUM output contains WARN" || fail "MEDIUM: WARN not in output"

# 5. git push -f (short form) should trigger MEDIUM
f=$(skill_file minus_f $'---\nname: minus-f\ndescription: minus-f\n---\nRun: git push -f origin feature-branch\n')
out=$(bash "$SCAN" "$f" 2>&1); rc=$?
[[ $rc -eq 0 ]] && ok "git push -f exits 0 (MEDIUM not HIGH)" || fail "git push -f: expected 0, got $rc"
echo "$out" | grep -qE "WARN|MEDIUM" && ok "git push -f triggers WARN" || fail "git push -f: expected WARN"

# 6. Edge case: git push -fast should NOT trigger (POSIX-ERE word boundary)
#    Pattern: 'git[[:space:]]+push[[:space:]]+-f($|[^[:alnum:]_-])'
#    "-fast" has 'a' after '-f', which is [[:alnum:]], so the boundary rejects it.
f=$(skill_file fast $'---\nname: fast\ndescription: fast\n---\nRun: git push -fast\n')
out=$(bash "$SCAN" "$f" 2>&1)
if echo "$out" | grep -qE "WARN|FAIL"; then
  fail "git push -fast incorrectly flagged (word boundary broken)"
else
  ok "git push -fast not flagged (POSIX-ERE word boundary works)"
fi

# 7. --json flag emits a valid JSON array
f=$(skill_file jsontest $'---\nname: jtest\ndescription: jtest\n---\nSafe content.\n')
out=$(bash "$SCAN" --json "$f" 2>&1); rc=$?
[[ $rc -eq 0 ]] && ok "--json exits 0 for clean file" || fail "--json: expected 0, got $rc"
json_part=$(echo "$out" | awk '/--- JSON ---/{found=1;next} found{print}')
if echo "$json_part" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
  ok "--json emits valid JSON array"
else
  fail "--json output is not valid JSON"
fi

echo ""
echo "============="
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && echo "PASSED" && exit 0
echo "FAILED"; exit 1
