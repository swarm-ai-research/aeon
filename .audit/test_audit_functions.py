"""
Tests for pure logic extracted from .audit/ processing scripts.
Run with: python -m pytest .audit/test_audit_functions.py
or:        python .audit/test_audit_functions.py
"""

import hashlib
import os
from collections import Counter

# ── our_severity ──────────────────────────────────────────────────────────────
# Duplicated from classify.py / extract_steps.py (scripts can't be imported
# without executing their top-level file I/O).

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


# ── fingerprint helper ────────────────────────────────────────────────────────
# From gen_trailer.py: spaces in step names are replaced with underscores.

def fp(rule, fname, step):
    s = f"{rule}|{os.path.basename(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── delta tagger ──────────────────────────────────────────────────────────────
# From delta3.py: for each (rule, file) pair, the first prior_count findings
# (sorted by line) are UNCHANGED; remainder are NEW.

def tag_delta(findings, prior_counts):
    """Mutates each finding in-place, adding 'delta' key."""
    import os
    def base(p):
        return os.path.basename(p)

    pairs = {(f['short_rule'], base(f['file'])) for f in findings}
    for (rule, fname) in pairs:
        pair_findings = sorted(
            [f for f in findings if f['short_rule'] == rule and base(f['file']) == fname],
            key=lambda x: x['line']
        )
        p = prior_counts.get((rule, fname), 0)
        for i, f in enumerate(pair_findings):
            f['delta'] = 'UNCHANGED' if i < p else 'NEW'
    return findings


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

def test_severity_critical():
    assert our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical'

def test_severity_critical_confidence_case_insensitive():
    # confidence is lower-cased inside our_severity
    assert our_severity({'level': 'error', 'confidence': 'High'}) == 'Critical'
    assert our_severity({'level': 'error', 'confidence': 'HIGH'}) == 'Critical'

def test_severity_high_error_low_confidence():
    assert our_severity({'level': 'error', 'confidence': 'low'}) == 'High'

def test_severity_high_error_empty_confidence():
    # empty confidence string: not 'high', so falls to second branch → High
    assert our_severity({'level': 'error', 'confidence': ''}) == 'High'

def test_severity_high_error_missing_confidence():
    # missing key: get() returns '' → same as empty
    assert our_severity({'level': 'error'}) == 'High'

def test_severity_high_warning_high_confidence():
    assert our_severity({'level': 'warning', 'confidence': 'high'}) == 'High'

def test_severity_medium_warning_low_confidence():
    assert our_severity({'level': 'warning', 'confidence': 'low'}) == 'Medium'

def test_severity_medium_warning_empty_confidence():
    assert our_severity({'level': 'warning', 'confidence': ''}) == 'Medium'

def test_severity_low_note_any_confidence():
    # note level always → Low regardless of confidence
    assert our_severity({'level': 'note', 'confidence': 'high'}) == 'Low'
    assert our_severity({'level': 'note', 'confidence': ''}) == 'Low'

def test_severity_low_unknown_level():
    # unknown level falls through all branches → Low
    assert our_severity({'level': 'unknown', 'confidence': 'high'}) == 'Low'
    assert our_severity({'level': ''}) == 'Low'


# ─────────────────────────────────────────────────────────────────────────────

def test_fp_deterministic():
    a = fp('unpinned-uses', '.github/workflows/aeon.yml', 'Checkout repo')
    b = fp('unpinned-uses', '.github/workflows/aeon.yml', 'Checkout repo')
    assert a == b

def test_fp_spaces_to_underscores():
    # "Checkout repo" and "Checkout_repo" should produce the same fingerprint
    a = fp('unpinned-uses', 'aeon.yml', 'Checkout repo')
    b = fp('unpinned-uses', 'aeon.yml', 'Checkout_repo')
    assert a == b

def test_fp_basename_only():
    # full path and basename should produce the same fingerprint
    a = fp('unpinned-uses', 'aeon.yml', 'step')
    b = fp('unpinned-uses', '.github/workflows/aeon.yml', 'step')
    assert a == b

def test_fp_distinct_for_different_inputs():
    a = fp('unpinned-uses', 'aeon.yml', 'step')
    b = fp('artipacked', 'aeon.yml', 'step')
    c = fp('unpinned-uses', 'other.yml', 'step')
    d = fp('unpinned-uses', 'aeon.yml', 'other step')
    assert len({a, b, c, d}) == 4

def test_fp_length():
    h = fp('rule', 'file.yml', 'step')
    assert len(h) == 16


# ─────────────────────────────────────────────────────────────────────────────

def _make_finding(rule, fname, line):
    return {'short_rule': rule, 'file': fname, 'line': line}

def test_delta_all_new_when_no_prior():
    findings = [_make_finding('artipacked', 'aeon.yml', i) for i in [10, 20, 30]]
    tag_delta(findings, prior_counts={})
    assert all(f['delta'] == 'NEW' for f in findings)

def test_delta_all_unchanged_when_prior_covers_all():
    findings = [_make_finding('artipacked', 'aeon.yml', i) for i in [10, 20, 30]]
    tag_delta(findings, prior_counts={('artipacked', 'aeon.yml'): 3})
    assert all(f['delta'] == 'UNCHANGED' for f in findings)

def test_delta_partial_new():
    # prior=2, today=3 → first 2 UNCHANGED, last 1 NEW
    findings = [_make_finding('artipacked', 'aeon.yml', i) for i in [10, 20, 30]]
    tag_delta(findings, prior_counts={('artipacked', 'aeon.yml'): 2})
    sorted_f = sorted(findings, key=lambda x: x['line'])
    assert sorted_f[0]['delta'] == 'UNCHANGED'
    assert sorted_f[1]['delta'] == 'UNCHANGED'
    assert sorted_f[2]['delta'] == 'NEW'

def test_delta_prior_exceeds_today():
    # prior=5, today=2 → both UNCHANGED (no negative NEW)
    findings = [_make_finding('artipacked', 'aeon.yml', i) for i in [10, 20]]
    tag_delta(findings, prior_counts={('artipacked', 'aeon.yml'): 5})
    assert all(f['delta'] == 'UNCHANGED' for f in findings)

def test_delta_independent_pairs():
    # Two separate (rule, file) pairs don't interfere
    findings = [
        _make_finding('artipacked', 'aeon.yml', 10),
        _make_finding('artipacked', 'aeon.yml', 20),
        _make_finding('unpinned-uses', 'aeon.yml', 30),
    ]
    tag_delta(findings, prior_counts={
        ('artipacked', 'aeon.yml'): 1,
        ('unpinned-uses', 'aeon.yml'): 0,
    })
    by_line = {f['line']: f['delta'] for f in findings}
    assert by_line[10] == 'UNCHANGED'
    assert by_line[20] == 'NEW'
    assert by_line[30] == 'NEW'

def test_delta_resolved_count():
    # prior=3, today=1 → resolved = 2 (today shows only 1 finding)
    findings = [_make_finding('artipacked', 'aeon.yml', 10)]
    tag_delta(findings, prior_counts={('artipacked', 'aeon.yml'): 3})
    # The single finding should be UNCHANGED (i < prior)
    assert findings[0]['delta'] == 'UNCHANGED'
    # Resolved count is prior - today = 3 - 1 = 2 (computed externally by caller)


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import sys
    passed = 0
    failed = 0
    tests = [(name, obj) for name, obj in sorted(globals().items())
             if name.startswith('test_') and callable(obj)]
    for name, fn in tests:
        try:
            fn()
            print(f'  ok  {name}')
            passed += 1
        except Exception as e:
            print(f'FAIL  {name}: {e}')
            failed += 1
    print(f'\n{passed} passed, {failed} failed')
    sys.exit(1 if failed else 0)
