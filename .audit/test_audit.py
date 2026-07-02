"""Tests for pure logic extracted from the audit pipeline scripts.

These functions are defined inline in classify.py / extract_steps.py / delta.py
but are copied verbatim here so they can be tested without triggering file I/O
at module import time.
"""

import hashlib
import os
import re


# ---------------------------------------------------------------------------
# Logic copied from classify.py / extract_steps.py (identical across both)
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


def make_fingerprint_classify(short_rule, file_path, snippet):
    """Fingerprint scheme used in classify.py."""
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(file_path)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Logic copied from delta.py
# ---------------------------------------------------------------------------

def fp_for_delta(rule, fname, step):
    """Fingerprint scheme used in delta.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def calibrate(findings):
    """Calibration override from delta.py / delta2.py / delta3.py."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


def short_rule_from_id(rule_id):
    return rule_id.split('/')[-1]


# ---------------------------------------------------------------------------
# our_severity — all five branches
# ---------------------------------------------------------------------------

def test_severity_critical():
    assert our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical'


def test_severity_critical_case_insensitive_confidence():
    assert our_severity({'level': 'error', 'confidence': 'High'}) == 'Critical'


def test_severity_high_error_low_confidence():
    assert our_severity({'level': 'error', 'confidence': 'low'}) == 'High'


def test_severity_high_error_no_confidence():
    assert our_severity({'level': 'error'}) == 'High'


def test_severity_high_warning_high_confidence():
    assert our_severity({'level': 'warning', 'confidence': 'high'}) == 'High'


def test_severity_medium_warning_low_confidence():
    assert our_severity({'level': 'warning', 'confidence': 'low'}) == 'Medium'


def test_severity_medium_warning_no_confidence():
    assert our_severity({'level': 'warning'}) == 'Medium'


def test_severity_low_note_level():
    assert our_severity({'level': 'note', 'confidence': 'high'}) == 'Low'


def test_severity_low_unknown_level():
    assert our_severity({'level': 'none'}) == 'Low'


def test_severity_low_empty_level():
    assert our_severity({'level': ''}) == 'Low'


# ---------------------------------------------------------------------------
# Fingerprint (classify.py scheme): format and stability
# ---------------------------------------------------------------------------

def test_classify_fingerprint_is_16_hex_chars():
    fp = make_fingerprint_classify('unpinned-uses', '.github/workflows/aeon.yml', 'uses: actions/checkout@v3')
    assert len(fp) == 16
    assert all(c in '0123456789abcdef' for c in fp)


def test_classify_fingerprint_stable():
    fp1 = make_fingerprint_classify('artipacked', 'workflows/ci.yml', 'run: echo hi')
    fp2 = make_fingerprint_classify('artipacked', 'workflows/ci.yml', 'run: echo hi')
    assert fp1 == fp2


def test_classify_fingerprint_uses_basename_only():
    fp_full = make_fingerprint_classify('artipacked', '/long/path/to/ci.yml', 'snippet')
    fp_base = make_fingerprint_classify('artipacked', 'ci.yml', 'snippet')
    assert fp_full == fp_base


def test_classify_fingerprint_snippet_truncated_to_60():
    long_snippet = 'a' * 100
    short_snippet = 'a' * 60
    fp_long = make_fingerprint_classify('rule', 'file.yml', long_snippet)
    fp_short = make_fingerprint_classify('rule', 'file.yml', short_snippet)
    assert fp_long == fp_short


def test_classify_fingerprint_snippet_whitespace_normalized():
    fp1 = make_fingerprint_classify('rule', 'f.yml', 'foo  bar\tbaz')
    fp2 = make_fingerprint_classify('rule', 'f.yml', 'foo bar baz')
    assert fp1 == fp2


def test_classify_fingerprint_differs_by_rule():
    fp1 = make_fingerprint_classify('rule-a', 'f.yml', 'snip')
    fp2 = make_fingerprint_classify('rule-b', 'f.yml', 'snip')
    assert fp1 != fp2


# ---------------------------------------------------------------------------
# Fingerprint (delta.py scheme): format and stability
# ---------------------------------------------------------------------------

def test_delta_fingerprint_is_16_hex_chars():
    fp = fp_for_delta('unpinned-uses', 'aeon.yml', 'Checkout')
    assert len(fp) == 16
    assert all(c in '0123456789abcdef' for c in fp)


def test_delta_fingerprint_stable():
    fp1 = fp_for_delta('artipacked', 'ci.yml', 'Build')
    fp2 = fp_for_delta('artipacked', 'ci.yml', 'Build')
    assert fp1 == fp2


def test_delta_fingerprint_uses_basename():
    fp_full = fp_for_delta('rule', '.github/workflows/ci.yml', 'step')
    fp_base = fp_for_delta('rule', 'ci.yml', 'step')
    assert fp_full == fp_base


def test_delta_fingerprint_step_change_changes_fingerprint():
    # Different step names for the same rule+file must produce different fingerprints
    # so that per-step deduplication in delta.py works correctly.
    fp1 = fp_for_delta('rule', 'ci.yml', 'Checkout')
    fp2 = fp_for_delta('rule', 'ci.yml', 'Build')
    assert fp1 != fp2


# ---------------------------------------------------------------------------
# Calibration override
# ---------------------------------------------------------------------------

def test_calibration_downgrades_unpinned_uses_critical():
    findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
    result = calibrate(findings)
    assert result[0]['severity'] == 'High'
    assert result[0]['calibrated'] is True


def test_calibration_leaves_unpinned_uses_high_unchanged():
    findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
    result = calibrate(findings)
    assert result[0]['severity'] == 'High'
    assert 'calibrated' not in result[0]


def test_calibration_leaves_other_critical_rules_unchanged():
    findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
    result = calibrate(findings)
    assert result[0]['severity'] == 'Critical'


def test_calibration_handles_empty_findings():
    assert calibrate([]) == []


# ---------------------------------------------------------------------------
# short_rule extraction
# ---------------------------------------------------------------------------

def test_short_rule_strips_namespace():
    assert short_rule_from_id('zizmor/unpinned-uses') == 'unpinned-uses'


def test_short_rule_no_namespace():
    assert short_rule_from_id('artipacked') == 'artipacked'


def test_short_rule_multiple_slashes():
    assert short_rule_from_id('a/b/c/rule-name') == 'rule-name'
