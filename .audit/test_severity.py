#!/usr/bin/env python3
"""Tests for the severity-classification and fingerprinting logic in classify.py and delta.py.

These scripts can't be imported (they run at module level), so the pure
functions are replicated here verbatim so every branch can be exercised.
"""
import hashlib
import os


# ── Replicated from classify.py ──────────────────────────────────────────────

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


# ── Replicated from delta.py ──────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_our_severity():
    cases = [
        # Critical: error + high confidence
        ({'level': 'error', 'confidence': 'high'}, 'Critical'),
        ({'level': 'error', 'confidence': 'High'}, 'Critical'),   # uppercase normalized by .lower()
        # High: error with non-high confidence
        ({'level': 'error', 'confidence': 'medium'}, 'High'),
        ({'level': 'error', 'confidence': 'low'}, 'High'),
        # High: error with missing confidence key — .get() defaults to '' → not 'high' → High not Critical
        ({'level': 'error'}, 'High'),
        ({'level': 'error', 'confidence': ''}, 'High'),
        # High: warning + high confidence
        ({'level': 'warning', 'confidence': 'high'}, 'High'),
        ({'level': 'warning', 'confidence': 'High'}, 'High'),
        # Medium: warning with non-high confidence
        ({'level': 'warning', 'confidence': 'medium'}, 'Medium'),
        ({'level': 'warning', 'confidence': 'low'}, 'Medium'),
        # Medium: warning with missing confidence key
        ({'level': 'warning'}, 'Medium'),
        # Low: note-level always falls through to the catch-all else
        ({'level': 'note', 'confidence': 'high'}, 'Low'),
        ({'level': 'note'}, 'Low'),
        # Low: any other level (info, unknown, empty)
        ({'level': 'info'}, 'Low'),
        ({'level': ''}, 'Low'),
    ]
    for finding, expected in cases:
        got = our_severity(finding)
        assert got == expected, f"our_severity({finding!r}) = {got!r}, want {expected!r}"
    print(f"OK  our_severity: {len(cases)} cases")


def test_fp_for_deterministic():
    fp = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
    assert len(fp) == 16, f"fingerprint must be 16 hex chars, got {len(fp)}"
    assert all(c in '0123456789abcdef' for c in fp), f"fingerprint must be lowercase hex: {fp!r}"
    assert fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node') == fp, \
        "identical inputs must produce the same fingerprint"
    print("OK  fp_for: deterministic 16-char hex")


def test_fp_for_basename_only():
    # delta.py strips the directory before hashing, matching how the prior-audit
    # trailer stores file basenames rather than full paths.
    fp_abs = fp_for('rule', '/repo/.github/workflows/ci.yml', 'step')
    fp_rel = fp_for('rule', '.github/workflows/ci.yml', 'step')
    fp_bare = fp_for('rule', 'ci.yml', 'step')
    assert fp_abs == fp_rel == fp_bare, (
        f"fp_for must hash only the basename; abs={fp_abs} rel={fp_rel} bare={fp_bare}"
    )
    print("OK  fp_for: path prefix stripped, only basename hashed")


def test_fp_for_field_sensitivity():
    # Each of the three fields must be distinguishable in the fingerprint.
    assert fp_for('rule-a', 'ci.yml', 'step') != fp_for('rule-b', 'ci.yml', 'step'), \
        "different rule should change fingerprint"
    assert fp_for('rule', 'ci.yml', 'step-a') != fp_for('rule', 'ci.yml', 'step-b'), \
        "different step should change fingerprint"
    assert fp_for('rule', 'ci.yml', 'step') != fp_for('rule', 'cd.yml', 'step'), \
        "different filename should change fingerprint"
    print("OK  fp_for: each field contributes to fingerprint uniqueness")


if __name__ == '__main__':
    test_our_severity()
    test_fp_for_deterministic()
    test_fp_for_basename_only()
    test_fp_for_field_sensitivity()
    print("\nAll .audit severity/fingerprint tests passed.")
