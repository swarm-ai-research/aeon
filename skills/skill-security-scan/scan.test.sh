#!/usr/bin/env bash
# scan.test.sh — Edge-case and boundary tests for scan.sh
#
# Covers:
#   - Severity-level exit codes (HIGH → 1, MEDIUM-only → 0, clean → 0)
#   - The POSIX-ERE -f word-boundary guard (no false-positive on -fast/-force)
#   - Distinction between force-push to main (HIGH) vs any branch (MEDIUM)
#   - Usage error path (no args → exit 2)
#   - Missing-file error path in scan_file()
#
# Run: bash skills/skill-security-scan/scan.test.sh

set -uo pipefail

SCAN="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/scan.sh"
PASS=0
FAIL=0

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

# Write a SKILL.md with the given content and return its path.
make_skill() {
  local name="$1" content="$2"
  local dir="$tmpdir/$name"
  mkdir -p "$dir"
  printf '%s\n' "$content" > "$dir/SKILL.md"
  echo "$dir/SKILL.md"
}

ok()   { PASS=$((PASS+1)); echo "OK  $1"; }
fail() { FAIL=$((FAIL+1)); echo "FAIL $1"; }

# 1. HIGH pattern → exit 1
f=$(make_skill "t1" 'Run: eval $USER_INPUT to process the request.')
bash "$SCAN" "$f" >/dev/null 2>&1; rc=$?
[ $rc -eq 1 ] \
  && ok "HIGH pattern (eval \$VAR) → exit 1" \
  || fail "HIGH pattern → exit 1 (got $rc)"

# 2. MEDIUM-only → exit 0 (WARN, not FAIL)
f=$(make_skill "t2" 'git reset --hard HEAD to discard changes')
bash "$SCAN" "$f" >/dev/null 2>&1; rc=$?
[ $rc -eq 0 ] \
  && ok "MEDIUM-only (git reset --hard) → exit 0" \
  || fail "MEDIUM-only → exit 0 (got $rc)"

# 3. git push -f is detected (MEDIUM → WARN, exit 0)
f=$(make_skill "t3" 'git push -f')
out=$(bash "$SCAN" "$f" 2>/dev/null); rc=$?
[ $rc -eq 0 ] && echo "$out" | grep -q 'WARN' \
  && ok "git push -f → WARN (MEDIUM detected, exit 0)" \
  || fail "git push -f not detected as MEDIUM (rc=$rc)"

# 4. git push -fast must NOT trigger the -f boundary pattern
#    The MEDIUM pattern uses ($|[^[:alnum:]_-]) so 'a' after -f must not match.
f=$(make_skill "t4" 'git push -fast to push a fast-forward update')
out=$(bash "$SCAN" "$f" 2>/dev/null); rc=$?
[ $rc -eq 0 ] && echo "$out" | grep -q 'PASS' && ! echo "$out" | grep -q 'WARN' \
  && ok "git push -fast: no false-positive on -f boundary" \
  || fail "git push -fast triggered false-positive (rc=$rc)"

# 5. Clean file → exit 0 with PASS status
f=$(make_skill "t5" 'Fetch public data from the GitHub API and write a summary.')
out=$(bash "$SCAN" "$f" 2>/dev/null); rc=$?
[ $rc -eq 0 ] && echo "$out" | grep -q 'PASS' \
  && ok "clean file → exit 0 (PASS)" \
  || fail "clean file → exit 0 PASS (rc=$rc)"

# 6. Missing file → non-zero exit (error path inside scan_file)
bash "$SCAN" "$tmpdir/no-such-dir/SKILL.md" >/dev/null 2>&1; rc=$?
[ $rc -ne 0 ] \
  && ok "missing file → non-zero exit" \
  || fail "missing file should fail (got $rc)"

# 7. No args → exit 2 (usage error)
bash "$SCAN" >/dev/null 2>&1; rc=$?
[ $rc -eq 2 ] \
  && ok "no args → exit 2 (usage)" \
  || fail "no args → exit 2 (got $rc)"

# 8. git push --force without origin/main → MEDIUM only (exit 0)
f=$(make_skill "t8" 'git push --force to update the feature branch')
out=$(bash "$SCAN" "$f" 2>/dev/null); rc=$?
[ $rc -eq 0 ] && echo "$out" | grep -q 'WARN' \
  && ok "git push --force (no origin main) → MEDIUM WARN, exit 0" \
  || fail "git push --force (no origin main) wrong result (rc=$rc)"

# 9. git push --force origin main → HIGH → exit 1
f=$(make_skill "t9" 'git push --force origin main')
bash "$SCAN" "$f" >/dev/null 2>&1; rc=$?
[ $rc -eq 1 ] \
  && ok "git push --force origin main → HIGH → exit 1" \
  || fail "git push --force origin main → exit 1 (got $rc)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ] && exit 0 || exit 1
