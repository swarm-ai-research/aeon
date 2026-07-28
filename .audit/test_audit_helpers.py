"""
Tests for the pure helper functions used in .audit/ processing scripts.

Covers: our_severity() (classify.py) and fp_for() (delta.py).
These are inlined here so the test has no import-time side-effects (the
original scripts open files unconditionally at module scope).

Run: python3 .audit/test_audit_helpers.py
"""
import hashlib
import os
import sys

passed = 0
failed = 0


def check(cond, label):
    global passed, failed
    if cond:
        passed += 1
        print(f"  OK  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}")


# ── our_severity (classify.py) ───────────────────────────────────────────────
# Maps SARIF level + zizmor confidence → our four-tier severity label.

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


print("our_severity:")

check(our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical',
      "error + high → Critical")

# Confidence values from the API sometimes arrive in mixed case.
check(our_severity({'level': 'error', 'confidence': 'High'}) == 'Critical',
      "error + 'High' (mixed case) → Critical (normalised via .lower())")

check(our_severity({'level': 'error', 'confidence': 'medium'}) == 'High',
      "error + medium confidence → High")

# Missing 'confidence' key — .get() must not raise; defaults to '' → non-high.
check(our_severity({'level': 'error'}) == 'High',
      "error + absent confidence key → High (not Critical)")

check(our_severity({'level': 'error', 'confidence': ''}) == 'High',
      "error + empty confidence string → High (not Critical)")

check(our_severity({'level': 'warning', 'confidence': 'high'}) == 'High',
      "warning + high → High")

check(our_severity({'level': 'warning', 'confidence': 'medium'}) == 'Medium',
      "warning + medium → Medium")

check(our_severity({'level': 'warning'}) == 'Medium',
      "warning + absent confidence key → Medium")

# 'note' level is never uplifted regardless of confidence.
check(our_severity({'level': 'note', 'confidence': 'high'}) == 'Low',
      "note + high confidence → Low (note is never uplifted)")

check(our_severity({'level': 'note'}) == 'Low',
      "note + absent confidence → Low")

# Unrecognised level falls through to the final return.
check(our_severity({'level': 'unknown-level', 'confidence': 'high'}) == 'Low',
      "unrecognised level → Low (safe fallthrough)")


# ── fp_for (delta.py) ────────────────────────────────────────────────────────
# Produces a 16-hex-char fingerprint from (rule, filename, step).
# Only the basename of the filename is used.

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


print("\nfp_for:")

check(len(fp_for('some-rule', 'ci.yml', 'Build')) == 16,
      "fingerprint length is always 16 chars")

check(all(c in '0123456789abcdef' for c in fp_for('r', 'f.yml', 's')),
      "fingerprint characters are lowercase hex only")

# The function strips the directory prefix: a full path must produce the same
# fingerprint as the bare filename so callers don't need to pre-strip paths.
check(
    fp_for('r', '.github/workflows/ci.yml', 's') == fp_for('r', 'ci.yml', 's'),
    "directory prefix is ignored — only basename affects the fingerprint",
)

# Different rules on the same file/step must not collide.
check(
    fp_for('rule-a', 'ci.yml', 'step') != fp_for('rule-b', 'ci.yml', 'step'),
    "different rules produce different fingerprints",
)

# delta.py documents that prior data stores step names with underscores while
# current findings use spaces (e.g. "Setup_Node" vs "Setup Node").  fp_for
# itself does NOT normalise — the caller must do it.  This test makes that
# contract explicit so future changes to fp_for don't silently break the delta.
check(
    fp_for('r', 'f.yml', 'Setup Node') != fp_for('r', 'f.yml', 'Setup_Node'),
    "spaces vs underscores in step names produce different fingerprints (caller must normalise)",
)

# Same inputs must always produce the same output (no randomness).
fp_a = fp_for('template-injection', 'deploy.yml', 'Publish')
fp_b = fp_for('template-injection', 'deploy.yml', 'Publish')
check(fp_a == fp_b, "fingerprint is deterministic for identical inputs")

# Edge case: all-empty inputs must still return a valid 16-char hex string.
check(len(fp_for('', '', '')) == 16,
      "all-empty inputs still produce a 16-char fingerprint")

print(f"\n{passed} passed, {failed} failed")
if failed:
    sys.exit(1)
