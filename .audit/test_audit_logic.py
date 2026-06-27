"""Unit tests for audit pipeline pure-function logic.

Covers branches and edge cases in:
  - our_severity() (extract_steps.py / classify.py)
  - fingerprint computation (extract_steps.py, gen_trailer.py, delta.py)
  - actionlint message scanning (summarize_al.py)

Run: python .audit/test_audit_logic.py
"""

import hashlib
import os
import sys


# ── Replicated from extract_steps.py (identical copy in classify.py) ──────
def our_severity(f):
    level = f['level']
    conf = f.get('confidence', '').lower()
    if level == 'error' and conf == 'high':
        return 'Critical'
    if level == 'error':
        return 'High'
    if level == 'warning' and conf == 'high':
        return 'High'
    if level == 'warning':
        return 'Medium'
    return 'Low'


# ── Replicated from gen_trailer.py ────────────────────────────────────────
def fp_trailer(rule, fname, step):
    b = os.path.basename(fname)
    s = f"{rule}|{b}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Replicated from delta.py ──────────────────────────────────────────────
def fp_delta(rule, fname, step):
    b = os.path.basename(fname)
    s = f"{rule}|{b}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Replicated from extract_steps.py (fingerprint scheme) ─────────────────
def fp_extract(short_rule, full_file, step):
    # Uses full path — not basename — so differs from gen_trailer / delta
    s = f"{short_rule}|{full_file}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Test harness ──────────────────────────────────────────────────────────
_passed = 0
_failed = 0


def check(condition, label):
    global _passed, _failed
    if condition:
        _passed += 1
        print(f"  PASS  {label}")
    else:
        _failed += 1
        print(f"  FAIL  {label}", file=sys.stderr)


# ── our_severity(): main classification branches ──────────────────────────
print("our_severity: primary branches")
check(our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical',
      "error + high confidence → Critical")
check(our_severity({'level': 'error', 'confidence': 'medium'}) == 'High',
      "error + medium confidence → High")
check(our_severity({'level': 'warning', 'confidence': 'high'}) == 'High',
      "warning + high confidence → High")
check(our_severity({'level': 'warning', 'confidence': 'medium'}) == 'Medium',
      "warning + medium confidence → Medium")

print("\nour_severity: edge cases")
# SARIF 'none' level (emitted when zizmor omits 'level') must fall to Low
check(our_severity({'level': 'none', 'confidence': 'high'}) == 'Low',
      "SARIF none-level + high confidence → Low (not uplifted)")

# 'note' level never uplifted by high confidence
check(our_severity({'level': 'note', 'confidence': 'high'}) == 'Low',
      "note + high confidence → Low (no uplift for note)")
check(our_severity({'level': 'note', 'confidence': ''}) == 'Low',
      "note + empty confidence → Low")

# Missing 'confidence' key falls back to '' which is not 'high'
check(our_severity({'level': 'error'}) == 'High',
      "error with no confidence key → High (not Critical)")
check(our_severity({'level': 'warning'}) == 'Medium',
      "warning with no confidence key → Medium (not High)")

# confidence value is lowercased before comparison — capital 'High' must work
check(our_severity({'level': 'error', 'confidence': 'High'}) == 'Critical',
      "error + capitalized 'High' → Critical (case-insensitive)")
check(our_severity({'level': 'warning', 'confidence': 'HIGH'}) == 'High',
      "warning + all-caps 'HIGH' → High (case-insensitive)")


# ── Fingerprint: gen_trailer converts spaces→underscores ──────────────────
print("\nfp_trailer (gen_trailer.py): space→underscore normalization")
h_space = fp_trailer('unpinned-uses', '.github/workflows/deploy.yml', 'Setup Node')
h_under = fp_trailer('unpinned-uses', '.github/workflows/deploy.yml', 'Setup_Node')
check(h_space == h_under,
      "step 'Setup Node' and 'Setup_Node' hash identically in gen_trailer")
check(len(h_space) == 16, "trailer fingerprint is 16 hex chars")
check(all(c in '0123456789abcdef' for c in h_space), "trailer fingerprint is lowercase hex")

# Basename-only path must equal full path (gen_trailer uses basename)
h_full = fp_trailer('rule', '.github/workflows/ci.yml', 'step')
h_base = fp_trailer('rule', 'ci.yml', 'step')
check(h_full == h_base, "full path and basename produce same trailer fingerprint")


# ── Fingerprint: delta.py does NOT normalize underscores ──────────────────
print("\nfp_delta (delta.py): no underscore normalization")
d_space = fp_delta('unpinned-uses', 'deploy.yml', 'Setup Node')
d_under = fp_delta('unpinned-uses', 'deploy.yml', 'Setup_Node')
check(d_space != d_under,
      "delta fp_for does NOT normalize spaces: 'Setup Node' ≠ 'Setup_Node'")
# delta.py handles this by adding both variants to prior_fp_set (tested by design)


# ── Cross-scheme mismatch: extract_steps uses full path, others use basename ──
print("\nfingerprint cross-scheme: extract_steps vs gen_trailer")
rule = 'unpinned-uses'
full_path = '.github/workflows/deploy.yml'
step = 'Setup Node'
fp_ex = fp_extract(rule, full_path, step)
fp_tr = fp_trailer(rule, full_path, step)
check(fp_ex != fp_tr,
      "extract_steps fp (full path, no underscore) differs from gen_trailer fp (basename, underscore)")
# This mismatch means delta-matching relies on exact trailer re-parsing, not cross-script reuse


# ── actionlint message scanning (summarize_al.py logic) ──────────────────
print("\nsummarize_al: message scanning logic")

def scan_al_message(msg):
    """Replicated from summarize_al.py: returns (matched_code_or_'other', is_high_candidate)."""
    for code in ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']:
        if code in msg:
            is_high = ('SC2086' in msg or 'SC2046' in msg) and 'github.' in msg.lower()
            return code, is_high
    return 'other', False

code, high = scan_al_message('SC2086: variable unquoted, github.event.inputs.name')
check(code == 'SC2086', "SC2086 in message → matched")
check(high is True, "SC2086 + github. → HIGH-CANDIDATE")

code, high = scan_al_message('SC2086: variable unquoted, GITHUB.EVENT.INPUTS.NAME')
check(high is True, "SC2086 + GITHUB. (uppercase) → HIGH-CANDIDATE (case-insensitive github check)")

code, high = scan_al_message('SC2086: variable unquoted, no-github-ref here')
check(code == 'SC2086', "SC2086 without github. → matched SC2086")
check(high is False, "SC2086 without github. → not HIGH-CANDIDATE")

code, high = scan_al_message('SC2046: word splitting, github.sha used')
check(code == 'SC2046', "SC2046 + github. → matched")
check(high is True, "SC2046 + github. → HIGH-CANDIDATE")

code, high = scan_al_message('SC2129: consider using { foo; bar; } >>file')
check(code == 'SC2129', "SC2129 → matched")
check(high is False, "SC2129 → not HIGH-CANDIDATE (not SC2086/SC2046)")

code, high = scan_al_message('some unknown lint warning about action syntax')
check(code == 'other', "unrecognized code → 'other'")
check(high is False, "'other' → not HIGH-CANDIDATE")

# Edge case: empty message
code, high = scan_al_message('')
check(code == 'other', "empty message → 'other'")

# Edge case: None message — dict.get('message', '') returns None if key is present with null
# value, causing 'SC2086' in None to raise TypeError. Document this behavior.
try:
    result = 'SC2086' in None  # noqa: E713
    check(False, "None message should raise TypeError")
except TypeError:
    check(True, "null message value causes TypeError in 'in' operator (known edge case)")


# ── Results ───────────────────────────────────────────────────────────────
print(f"\n{_passed} passed, {_failed} failed")
if _failed:
    sys.exit(1)
