"""Tests for audit classification and fingerprint logic.

These functions live inline in the audit scripts; we replicate them here
to get coverage without modifying production code.
"""

import hashlib
import os
import re


# --- replicated from classify.py / extract_steps.py ---

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


# --- replicated from gen_trailer.py ---

def fp_trailer(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# --- replicated from delta.py ---

def fp_delta(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# --- replicated from classify.py snippet-based fingerprint ---

def fp_snippet(short_rule, file_path, snippet):
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(file_path)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ============================================================
# our_severity tests
# ============================================================

def test_error_high_confidence_is_critical():
    assert our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical'


def test_error_high_confidence_case_insensitive():
    assert our_severity({'level': 'error', 'confidence': 'HIGH'}) == 'Critical'
    assert our_severity({'level': 'error', 'confidence': 'High'}) == 'Critical'


def test_error_low_confidence_is_high():
    assert our_severity({'level': 'error', 'confidence': 'low'}) == 'High'


def test_error_medium_confidence_is_high():
    assert our_severity({'level': 'error', 'confidence': 'medium'}) == 'High'


def test_error_missing_confidence_is_high():
    # No 'confidence' key at all — should not raise, should return High
    assert our_severity({'level': 'error'}) == 'High'


def test_warning_high_confidence_is_high():
    assert our_severity({'level': 'warning', 'confidence': 'high'}) == 'High'


def test_warning_low_confidence_is_medium():
    assert our_severity({'level': 'warning', 'confidence': 'low'}) == 'Medium'


def test_warning_missing_confidence_is_medium():
    assert our_severity({'level': 'warning'}) == 'Medium'


def test_note_is_low():
    assert our_severity({'level': 'note'}) == 'Low'


def test_note_with_high_confidence_is_still_low():
    # Only error/warning levels are promoted by confidence
    assert our_severity({'level': 'note', 'confidence': 'high'}) == 'Low'


def test_unknown_level_falls_through_to_low():
    assert our_severity({'level': 'info', 'confidence': 'high'}) == 'Low'


# ============================================================
# fingerprint consistency tests
# ============================================================

def test_fp_trailer_produces_16_hex_chars():
    result = fp_trailer('unpinned-uses', '.github/workflows/aeon.yml', 'Setup Node')
    assert len(result) == 16
    assert all(c in '0123456789abcdef' for c in result)


def test_fp_delta_produces_16_hex_chars():
    result = fp_delta('unpinned-uses', '.github/workflows/aeon.yml', 'Setup Node')
    assert len(result) == 16
    assert all(c in '0123456789abcdef' for c in result)


def test_fp_trailer_vs_delta_differ_on_spaces():
    # trailer replaces spaces with underscores; delta does not.
    # The two schemes therefore produce different hashes for the same inputs.
    step = 'Setup Node'
    a = fp_trailer('r', 'f.yml', step)
    b = fp_delta('r', 'f.yml', step)
    assert a != b, "trailer (underscore) and delta (space) fingerprints must differ"


def test_fp_trailer_stable():
    # Fingerprints must not change across runs (they index prior audits).
    expected = fp_trailer('unpinned-uses', 'aeon.yml', 'Checkout')
    assert fp_trailer('unpinned-uses', 'aeon.yml', 'Checkout') == expected


def test_fp_uses_basename_only():
    a = fp_trailer('rule', '.github/workflows/lint.yml', 'step')
    b = fp_trailer('rule', 'lint.yml', 'step')
    assert a == b, "fingerprint must be path-agnostic (basename only)"


def test_fp_delta_uses_basename_only():
    a = fp_delta('rule', '.github/workflows/lint.yml', 'step')
    b = fp_delta('rule', 'lint.yml', 'step')
    assert a == b


def test_fp_snippet_truncates_at_60():
    long_snippet = 'x' * 100
    short_snippet = 'x' * 60
    a = fp_snippet('rule', 'f.yml', long_snippet)
    b = fp_snippet('rule', 'f.yml', short_snippet)
    assert a == b, "snippet fingerprint should use only first 60 chars"


def test_fp_snippet_collapses_whitespace():
    a = fp_snippet('rule', 'f.yml', 'foo   bar')
    b = fp_snippet('rule', 'f.yml', 'foo bar')
    assert a == b, "snippet fingerprint should collapse internal whitespace"


# ============================================================
# calibration / override logic
# ============================================================

def apply_calibration(findings):
    """Mirrors the calibration overrides from delta.py and finalize.py."""
    for f in findings:
        # delta.py: unpinned-uses error-level stays High, not Critical
        if f.get('short_rule') == 'unpinned-uses' and f.get('severity') == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
        # finalize.py: secrets-outside-env downgraded High -> Medium
        if f.get('short_rule') == 'secrets-outside-env' and f.get('severity') == 'High':
            f['severity'] = 'Medium'
    return findings


def test_calibration_unpinned_uses_critical_becomes_high():
    f = {'short_rule': 'unpinned-uses', 'severity': 'Critical'}
    result = apply_calibration([f])
    assert result[0]['severity'] == 'High'
    assert result[0].get('calibrated') is True


def test_calibration_unpinned_uses_high_stays_high():
    f = {'short_rule': 'unpinned-uses', 'severity': 'High'}
    result = apply_calibration([f])
    assert result[0]['severity'] == 'High'
    assert 'calibrated' not in result[0]


def test_calibration_secrets_outside_env_high_becomes_medium():
    f = {'short_rule': 'secrets-outside-env', 'severity': 'High'}
    result = apply_calibration([f])
    assert result[0]['severity'] == 'Medium'


def test_calibration_secrets_outside_env_medium_unchanged():
    f = {'short_rule': 'secrets-outside-env', 'severity': 'Medium'}
    result = apply_calibration([f])
    assert result[0]['severity'] == 'Medium'


def test_calibration_other_rules_unaffected():
    f = {'short_rule': 'template-injection', 'severity': 'Critical'}
    result = apply_calibration([f])
    assert result[0]['severity'] == 'Critical'


def test_calibration_multiple_findings_independent():
    findings = [
        {'short_rule': 'unpinned-uses', 'severity': 'Critical'},
        {'short_rule': 'secrets-outside-env', 'severity': 'High'},
        {'short_rule': 'template-injection', 'severity': 'High'},
    ]
    result = apply_calibration(findings)
    assert result[0]['severity'] == 'High'
    assert result[1]['severity'] == 'Medium'
    assert result[2]['severity'] == 'High'


# ============================================================
# runner
# ============================================================

if __name__ == '__main__':
    import sys
    tests = [(k, v) for k, v in globals().items() if k.startswith('test_') and callable(v)]
    failed = []
    for name, fn in tests:
        try:
            fn()
            print(f'  OK  {name}')
        except Exception as e:
            print(f'FAIL  {name}: {e}')
            failed.append(name)
    print(f'\n{len(tests) - len(failed)}/{len(tests)} passed')
    sys.exit(len(failed))
