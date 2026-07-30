"""
Tests for pure logic extracted from .audit/*.py scripts.

The scripts are not importable modules, so the functions are re-defined here
verbatim from the source they originate from.  If a function changes, update
the copy below and the test that validates the new behaviour.

Run with:  python -m pytest .audit/test_audit_logic.py -v
"""

import hashlib
import os
import unittest


# ---------------------------------------------------------------------------
# Functions under test (copied verbatim from classify.py / extract_steps.py)
# ---------------------------------------------------------------------------

def our_severity(f):
    """Severity mapping used in classify.py and extract_steps.py."""
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
    """Fingerprint function copied verbatim from delta.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Calibration helpers (from delta.py and finalize.py)
# ---------------------------------------------------------------------------

def apply_delta_calibration(findings):
    """Calibrate unpinned-uses: policy-level error -> High, not Critical."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


def apply_finalize_calibration(findings):
    """Calibrate secrets-outside-env: High -> Medium."""
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium'
            )
    return findings


# ---------------------------------------------------------------------------
# Delta-tagging helper (from delta3.py)
# ---------------------------------------------------------------------------

def tag_findings_delta(findings, prior_counts):
    """
    For each (rule, basename) pair, the first prior_count findings (sorted by
    line) are tagged UNCHANGED; the rest NEW.  Mutates findings in-place.
    """
    pairs = {(f['short_rule'], os.path.basename(f['file'])) for f in findings}
    for rule, fname in pairs:
        pair_findings = sorted(
            [f for f in findings
             if f['short_rule'] == rule and os.path.basename(f['file']) == fname],
            key=lambda x: x['line'],
        )
        p = prior_counts.get((rule, fname), 0)
        for i, f in enumerate(pair_findings):
            f['delta'] = 'UNCHANGED' if i < p else 'NEW'
    return findings


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestOurSeverity(unittest.TestCase):

    def _f(self, level, confidence=''):
        return {'level': level, 'confidence': confidence}

    # Critical path
    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity(self._f('error', 'high')), 'Critical')

    def test_error_high_confidence_case_insensitive(self):
        # confidence is lowercased inside the function
        self.assertEqual(our_severity(self._f('error', 'High')), 'Critical')
        self.assertEqual(our_severity(self._f('error', 'HIGH')), 'Critical')

    # High paths
    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'low')), 'High')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'medium')), 'High')

    def test_error_no_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error')), 'High')

    def test_error_missing_confidence_key_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('warning', 'high')), 'High')

    # Medium paths
    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'medium')), 'Medium')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'low')), 'Medium')

    def test_warning_no_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning')), 'Medium')

    # Low paths — note level is always Low regardless of confidence
    def test_note_high_confidence_is_low(self):
        self.assertEqual(our_severity(self._f('note', 'high')), 'Low')

    def test_note_no_confidence_is_low(self):
        self.assertEqual(our_severity(self._f('note')), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity(self._f('unknown_level', 'high')), 'Low')


class TestFpFor(unittest.TestCase):

    def test_returns_16_hex_chars(self):
        fp = fp_for('unpinned-uses', 'aeon.yml', 'Checkout')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_deterministic(self):
        a = fp_for('artipacked', '.github/workflows/aeon.yml', 'Setup Node')
        b = fp_for('artipacked', '.github/workflows/aeon.yml', 'Setup Node')
        self.assertEqual(a, b)

    def test_full_path_reduces_to_basename(self):
        fp_full = fp_for('artipacked', '/home/runner/work/.github/workflows/aeon.yml', 'Setup Node')
        fp_base = fp_for('artipacked', 'aeon.yml', 'Setup Node')
        self.assertEqual(fp_full, fp_base)

    def test_different_rule_gives_different_fp(self):
        a = fp_for('artipacked', 'aeon.yml', 'Setup Node')
        b = fp_for('unpinned-uses', 'aeon.yml', 'Setup Node')
        self.assertNotEqual(a, b)

    def test_different_step_gives_different_fp(self):
        a = fp_for('artipacked', 'aeon.yml', 'Setup Node')
        b = fp_for('artipacked', 'aeon.yml', 'Checkout')
        self.assertNotEqual(a, b)

    def test_different_file_same_basename_gives_same_fp(self):
        a = fp_for('artipacked', 'dir1/aeon.yml', 'top')
        b = fp_for('artipacked', 'dir2/aeon.yml', 'top')
        self.assertEqual(a, b)


class TestDeltaCalibration(unittest.TestCase):

    def _finding(self, rule, severity):
        return {'short_rule': rule, 'severity': severity}

    def test_unpinned_uses_critical_downgraded_to_high(self):
        f = self._finding('unpinned-uses', 'Critical')
        apply_delta_calibration([f])
        self.assertEqual(f['severity'], 'High')
        self.assertTrue(f.get('calibrated'))

    def test_other_rule_critical_not_touched(self):
        f = self._finding('secrets-outside-env', 'Critical')
        apply_delta_calibration([f])
        self.assertEqual(f['severity'], 'Critical')

    def test_unpinned_uses_high_not_touched(self):
        f = self._finding('unpinned-uses', 'High')
        apply_delta_calibration([f])
        self.assertEqual(f['severity'], 'High')
        self.assertFalse(f.get('calibrated', False))

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        f = self._finding('secrets-outside-env', 'High')
        apply_finalize_calibration([f])
        self.assertEqual(f['severity'], 'Medium')

    def test_secrets_outside_env_medium_not_touched(self):
        f = self._finding('secrets-outside-env', 'Medium')
        apply_finalize_calibration([f])
        self.assertEqual(f['severity'], 'Medium')

    def test_artipacked_high_not_touched_by_finalize(self):
        f = self._finding('artipacked', 'High')
        apply_finalize_calibration([f])
        self.assertEqual(f['severity'], 'High')


class TestDeltaTagging(unittest.TestCase):

    def _mk(self, rule, fname, line):
        return {'short_rule': rule, 'file': fname, 'line': line, 'delta': None}

    def test_all_new_when_no_prior(self):
        findings = [self._mk('artipacked', 'aeon.yml', i) for i in [10, 20, 30]]
        tag_findings_delta(findings, {})
        self.assertTrue(all(f['delta'] == 'NEW' for f in findings))

    def test_all_unchanged_when_prior_covers_all(self):
        findings = [self._mk('artipacked', 'aeon.yml', i) for i in [10, 20, 30]]
        tag_findings_delta(findings, {('artipacked', 'aeon.yml'): 3})
        self.assertTrue(all(f['delta'] == 'UNCHANGED' for f in findings))

    def test_first_n_unchanged_rest_new(self):
        findings = [self._mk('artipacked', 'aeon.yml', i) for i in [10, 20, 30, 40]]
        tag_findings_delta(findings, {('artipacked', 'aeon.yml'): 2})
        by_line = sorted(findings, key=lambda f: f['line'])
        self.assertEqual(by_line[0]['delta'], 'UNCHANGED')
        self.assertEqual(by_line[1]['delta'], 'UNCHANGED')
        self.assertEqual(by_line[2]['delta'], 'NEW')
        self.assertEqual(by_line[3]['delta'], 'NEW')

    def test_prior_count_zero_all_new(self):
        findings = [self._mk('unpinned-uses', 'messages.yml', i) for i in [5, 15]]
        tag_findings_delta(findings, {('unpinned-uses', 'messages.yml'): 0})
        self.assertTrue(all(f['delta'] == 'NEW' for f in findings))

    def test_tagging_is_by_line_order(self):
        # Findings provided out of order — tagging uses line-sorted order
        findings = [
            self._mk('artipacked', 'aeon.yml', 50),
            self._mk('artipacked', 'aeon.yml', 10),  # lowest line → UNCHANGED
            self._mk('artipacked', 'aeon.yml', 30),
        ]
        tag_findings_delta(findings, {('artipacked', 'aeon.yml'): 1})
        by_line = {f['line']: f['delta'] for f in findings}
        self.assertEqual(by_line[10], 'UNCHANGED')
        self.assertEqual(by_line[30], 'NEW')
        self.assertEqual(by_line[50], 'NEW')

    def test_independent_rules_tagged_separately(self):
        findings = [
            self._mk('artipacked', 'aeon.yml', 10),
            self._mk('unpinned-uses', 'aeon.yml', 20),
        ]
        prior = {('artipacked', 'aeon.yml'): 1, ('unpinned-uses', 'aeon.yml'): 0}
        tag_findings_delta(findings, prior)
        by_rule = {f['short_rule']: f['delta'] for f in findings}
        self.assertEqual(by_rule['artipacked'], 'UNCHANGED')
        self.assertEqual(by_rule['unpinned-uses'], 'NEW')


if __name__ == '__main__':
    unittest.main()
