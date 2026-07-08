#!/usr/bin/env bash
# scan.test.sh — Tests for skills/skill-security-scan/scan.sh
#
# Run: bash skills/skill-security-scan/scan.test.sh
#
# Covers:
#   - clean file → exit 0 / PASS
#   - high-severity file → exit 1 / HIGH
#   - medium-only file → exit 0 / WARN with MEDIUM label
#   - edge case: `git push -f` at end-of-line matches MEDIUM
#   - edge case: `git push -force` (one dash, word continues) does NOT match -f pattern
#   - --json flag produces valid JSON
#   - no args → exit 2 (usage error)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCAN="$SCRIPT_DIR/scan.sh"

PASS=0
FAIL=0

ok()   { echo "PASS: $1"; PASS=$((PASS+1)); }
fail() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }

check_exit() {
  local label="$1" expected="$2"
  shift 2
  local actual=0
  "$@" >/dev/null 2>&1 || actual=$?
  if [[ $actual -eq $expected ]]; then ok "$label"; else fail "$label (expected=$expected actual=$actual)"; fi
}

check_output_has() {
  local label="$1" needle="$2"
  shift 2
  local out
  out=$("$@" 2>&1) || true
  if grep -qF "$needle" <<< "$out"; then ok "$label"; else fail "$label (needle='$needle' not found in output)"; fi
}

check_output_lacks() {
  local label="$1" needle="$2"
  shift 2
  local out
  out=$("$@" 2>&1) || true
  if ! grep -qF "$needle" <<< "$out"; then ok "$label"; else fail "$label (needle='$needle' found but should be absent)"; fi
}

TMPD="$(mktemp -d)"
trap 'rm -rf "$TMPD"' EXIT

# Helper: create a fake SKILL.md with the given body; echo its path.
make_skill() {
  local name="$1" body="$2"
  local path="$TMPD/${name}/SKILL.md"
  mkdir -p "$(dirname "$path")"
  printf '%s\n' "$body" > "$path"
  echo "$path"
}

CLEAN=$(make_skill "clean"   "# Clean Skill\necho hello world")
HIGH=$(make_skill  "evil"    "# Evil Skill\neval \$USER_INPUT")
MEDIUM=$(make_skill "medium" "# Medium Skill\ngit push --force origin/feature-branch")

# git push -f at end-of-line: the MEDIUM pattern `git push -f($|[^alnum_-])` should match.
F_EOL=$(make_skill "push-f-eol" "$(printf '# Push EOL\ngit push -f')")

# git push -force (one dash, word continues with 'o'): the -f pattern requires -f at EOL
# or followed by a non-alnum/underscore/dash character, so 'o' after -f should NOT match.
F_SUFFIX=$(make_skill "push-f-suffix" "$(printf '# Push -force\ngit push -force origin')")

# --- exit code checks ---
check_exit "clean file exits 0"       0 bash "$SCAN" "$CLEAN"
check_exit "high-sev file exits 1"    1 bash "$SCAN" "$HIGH"
check_exit "medium-only file exits 0" 0 bash "$SCAN" "$MEDIUM"
check_exit "no args exits 2"          2 bash "$SCAN"

# --- output label checks ---
check_output_has  "clean file emits PASS"         "PASS"   bash "$SCAN" "$CLEAN"
check_output_has  "high-sev file emits HIGH"      "HIGH"   bash "$SCAN" "$HIGH"
check_output_has  "medium-only file emits MEDIUM" "MEDIUM" bash "$SCAN" "$MEDIUM"

# --- edge case: git push -f at end-of-line triggers MEDIUM (not HIGH) ---
check_output_has  "git push -f at EOL is flagged MEDIUM" "MEDIUM" bash "$SCAN" "$F_EOL"
check_exit        "git push -f at EOL exits 0 (WARN not FAIL)" 0 bash "$SCAN" "$F_EOL"

# --- edge case: git push -force (word boundary not met) passes clean ---
check_exit        "git push -force does not trigger -f pattern (exits 0)" 0 bash "$SCAN" "$F_SUFFIX"
check_output_lacks "git push -force does not emit MEDIUM" "MEDIUM" bash "$SCAN" "$F_SUFFIX"

# --- --json flag produces valid JSON (requires jq) ---
if command -v jq >/dev/null 2>&1; then
  JSON_SECTION=$(bash "$SCAN" --json "$CLEAN" 2>&1 | awk '/^--- JSON ---/{p=1;next} p')
  if [[ -n "$JSON_SECTION" ]] && echo "$JSON_SECTION" | python3 -c "import sys,json; json.loads(sys.stdin.read())" 2>/dev/null; then
    ok "--json flag produces valid JSON"
  else
    fail "--json flag produces valid JSON"
  fi
else
  echo "SKIP: --json test (jq not available)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
