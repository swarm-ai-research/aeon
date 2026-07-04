"""
Tests for audit classification logic — severity mapping and fingerprinting.

Covers the our_severity() logic from classify.py and the fp_for() logic from
delta.py, which both process output from .audit-bin/actionlint and
.audit-bin/zizmor.

Run: python .audit/test_audit_logic.py
"""

import hashlib
import os

# ---------------------------------------------------------------------------
# Reference implementations (mirrors classify.py / delta.py exactly)
# ---------------------------------------------------------------------------

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


def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------

passed = failed = 0


def check(cond, label):
    global passed, failed
    if cond:
        passed += 1
        print(f"  OK  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}")


# ---------------------------------------------------------------------------
# our_severity — edge cases
# ---------------------------------------------------------------------------

print("our_severity:")

# Critical branch
check(our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical',
      "error + high → Critical")
check(our_severity({'level': 'error', 'confidence': 'HIGH'}) == 'Critical',
      "error + HIGH (upper) → Critical (confidence lowercased before compare)")

# High branch — error with non-high confidence
check(our_severity({'level': 'error', 'confidence': 'medium'}) == 'High',
      "error + medium → High (not Critical)")
check(our_severity({'level': 'error', 'confidence': ''}) == 'High',
      "error + empty confidence → High")
check(our_severity({'level': 'error'}) == 'High',
      "error + missing confidence key → High (defaults to '')")

# High branch — warning + high
check(our_severity({'level': 'warning', 'confidence': 'high'}) == 'High',
      "warning + high → High")

# Medium branch — warning with non-high confidence
check(our_severity({'level': 'warning', 'confidence': 'medium'}) == 'Medium',
      "warning + medium → Medium")
check(our_severity({'level': 'warning', 'confidence': ''}) == 'Medium',
      "warning + empty confidence → Medium")
check(our_severity({'level': 'warning'}) == 'Medium',
      "warning + missing confidence key → Medium")

# Low branch — note is always Low even with high confidence
check(our_severity({'level': 'note', 'confidence': 'high'}) == 'Low',
      "note + high → Low (note-level never elevated)")
check(our_severity({'level': 'note', 'confidence': 'medium'}) == 'Low',
      "note + medium → Low")
check(our_severity({'level': 'note'}) == 'Low',
      "note + missing confidence → Low")
check(our_severity({'level': 'none'}) == 'Low',
      "unknown level → Low (falls to else)")

# ---------------------------------------------------------------------------
# fp_for — fingerprinting properties
# ---------------------------------------------------------------------------

print("\nfp_for:")

# Deterministic
check(fp_for('rule-a', 'workflow.yml', 'step') == fp_for('rule-a', 'workflow.yml', 'step'),
      "same inputs → same fingerprint (deterministic)")

# Different inputs produce different fingerprints
check(fp_for('rule-a', 'workflow.yml', 'step') != fp_for('rule-b', 'workflow.yml', 'step'),
      "different rule → different fingerprint")
check(fp_for('rule-a', 'a.yml', 'step') != fp_for('rule-a', 'b.yml', 'step'),
      "different filename → different fingerprint")
check(fp_for('rule-a', 'workflow.yml', 'step1') != fp_for('rule-a', 'workflow.yml', 'step2'),
      "different step → different fingerprint")

# Output format: always 16 lowercase hex chars
fp = fp_for('injection/template-injection', '.github/workflows/ci.yml', 'Build step')
check(len(fp) == 16, f"fingerprint length is 16 (got {len(fp)})")
check(all(c in '0123456789abcdef' for c in fp), "fingerprint is lowercase hex")

# Basename extraction — different full paths with same filename collapse to the same fp
check(fp_for('rule', '/path/to/workflow.yml', 'step') == fp_for('rule', 'other/workflow.yml', 'step'),
      "fp_for uses basename — full paths with same filename match")
check(fp_for('rule', '/a/b/c.yml', 'step') != fp_for('rule', '/a/b/d.yml', 'step'),
      "different basenames remain distinct")

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
