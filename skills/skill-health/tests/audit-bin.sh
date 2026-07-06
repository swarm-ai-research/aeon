#!/usr/bin/env bash
# audit-bin.sh — Verify .audit-bin/ scanner binaries are present, executable, and intact.
#
# These binaries are committed as a sandbox workaround (piped-curl installs are
# blocked in CI). If they lose their execute bit or get corrupted, the audit skill
# silently degrades to hand-rolled fallbacks with no warning.
#
# Usage: ./skills/skill-health/tests/audit-bin.sh
# Exit codes:
#   0 = all checks passed
#   1 = one or more checks failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AUDIT_BIN="$REPO_ROOT/.audit-bin"

FAIL_COUNT=0
PASS_COUNT=0

pass() { echo "  PASS $1"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { echo "  FAIL $1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }

elf_magic() {
  # Returns the first 4 bytes as lowercase hex (e.g. "7f454c46" for ELF).
  # Uses od -An -tx1 which is POSIX-portable.
  dd if="$1" bs=4 count=1 2>/dev/null | od -An -tx1 | tr -d ' \n'
}

echo "Audit-bin integrity checks"
echo "=========================="
echo ""

# ── 1. Directory ────────────────────────────────────────────────────────────
echo ".audit-bin/ directory"
if [[ -d "$AUDIT_BIN" ]]; then
  pass ".audit-bin/ directory exists"
else
  fail ".audit-bin/ directory missing — scanners cannot be used from prefetch cache"
  echo ""
  echo "FAIL: 1 check failed"
  exit 1
fi

# ── 2. actionlint binary ─────────────────────────────────────────────────────
echo ""
echo "actionlint binary"
if [[ -f "$AUDIT_BIN/actionlint" ]]; then
  pass "actionlint present"
  if [[ -x "$AUDIT_BIN/actionlint" ]]; then
    pass "actionlint is executable"
  else
    fail "actionlint is not executable — git may have stripped the execute bit (chmod +x .audit-bin/actionlint)"
  fi
  magic=$(elf_magic "$AUDIT_BIN/actionlint")
  if [[ "$magic" == "7f454c46" ]]; then
    pass "actionlint ELF magic bytes correct"
  else
    fail "actionlint does not appear to be an ELF binary (magic bytes: ${magic:-<empty>})"
  fi
else
  fail "actionlint missing from .audit-bin/"
fi

# ── 3. zizmor binary ─────────────────────────────────────────────────────────
echo ""
echo "zizmor binary"
if [[ -f "$AUDIT_BIN/zizmor" ]]; then
  pass "zizmor present"
  if [[ -x "$AUDIT_BIN/zizmor" ]]; then
    pass "zizmor is executable"
  else
    fail "zizmor is not executable — git may have stripped the execute bit (chmod +x .audit-bin/zizmor)"
  fi
  magic=$(elf_magic "$AUDIT_BIN/zizmor")
  if [[ "$magic" == "7f454c46" ]]; then
    pass "zizmor ELF magic bytes correct"
  else
    fail "zizmor does not appear to be an ELF binary (magic bytes: ${magic:-<empty>})"
  fi
else
  fail "zizmor missing from .audit-bin/"
fi

# ── 4. actionlint.tar.gz ─────────────────────────────────────────────────────
echo ""
echo "actionlint.tar.gz"
if [[ -f "$AUDIT_BIN/actionlint.tar.gz" ]]; then
  pass "actionlint.tar.gz present"
else
  fail "actionlint.tar.gz missing from .audit-bin/"
fi

if [[ -f "$AUDIT_BIN/actionlint.tar.gz" ]]; then
  if tar tf "$AUDIT_BIN/actionlint.tar.gz" >/dev/null 2>&1; then
    pass "actionlint.tar.gz is a valid gzip archive"
    # Edge case: archive exists but the binary entry was removed or renamed
    if tar tf "$AUDIT_BIN/actionlint.tar.gz" 2>/dev/null | grep -qE '(^|/)actionlint$'; then
      pass "actionlint.tar.gz contains an actionlint entry"
    else
      fail "actionlint.tar.gz does not contain an 'actionlint' entry — archive may be wrong version or corrupt"
    fi
  else
    fail "actionlint.tar.gz failed tar integrity check — file may be truncated or corrupt"
  fi
fi

# ── 5. No unexpected extra files ─────────────────────────────────────────────
echo ""
echo "directory contents"
unexpected=()
while IFS= read -r f; do
  base="$(basename "$f")"
  case "$base" in
    actionlint|actionlint.tar.gz|zizmor) ;;
    *) unexpected+=("$base") ;;
  esac
done < <(find "$AUDIT_BIN" -maxdepth 1 -type f)

if [[ ${#unexpected[@]} -eq 0 ]]; then
  pass "no unexpected files in .audit-bin/"
else
  for u in "${unexpected[@]}"; do
    fail "unexpected file in .audit-bin/: $u"
  done
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "=========================="
echo "Checks passed: $PASS_COUNT"
if [[ $FAIL_COUNT -gt 0 ]]; then
  echo "Checks failed: $FAIL_COUNT"
  exit 1
fi
echo "All audit-bin checks passed."
exit 0
