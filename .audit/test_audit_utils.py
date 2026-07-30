"""
Tests for pure utility functions extracted from .audit/ processing scripts.
Run with: python3 -m pytest .audit/test_audit_utils.py -v
  or:       python3 .audit/test_audit_utils.py
"""

import hashlib
import os
import unittest


# ── Replicated from classify.py / extract_steps.py ──────────────────────────

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


# ── Replicated from delta.py ─────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Replicated from gen_trailer.py ──────────────────────────────────────────

def fp_trailer(rule, fname, step):
    """Trailer variant: spaces in step names become underscores."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Replicated calibration overrides (delta.py / delta3.py / finalize.py) ───

def apply_unpinned_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


def apply_secrets_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
    return findings


# ── Replicated delta classification (delta3.py) ──────────────────────────────

def classify_delta(findings, prior_counts):
    """Tag each finding NEW or UNCHANGED.

    For each (short_rule, basename(file)) pair, the first prior_counts[pair]
    findings (sorted by line ascending) are UNCHANGED; the rest are NEW.
    """
    def base(p):
        return os.path.basename(p)

    pairs = {(f['short_rule'], base(f['file'])) for f in findings}
    for (rule, fname) in pairs:
        pair_findings = sorted(
            [f for f in findings if f['short_rule'] == rule and base(f['file']) == fname],
            key=lambda x: x['line'],
        )
        p = prior_counts.get((rule, fname), 0)
        for i, f in enumerate(pair_findings):
            f['delta'] = 'UNCHANGED' if i < p else 'NEW'
    return findings


# ─────────────────────────────────────────────────────────────────────────────


class TestOurSeverity(unittest.TestCase):

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_confidence_case_insensitive(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_missing_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info'}), 'Low')


class TestFingerprint(unittest.TestCase):

    def test_fp_for_is_16_hex_chars(self):
        result = fp_for('artipacked', '.github/workflows/aeon.yml', 'Checkout')
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_fp_for_is_deterministic(self):
        a = fp_for('unpinned-uses', 'fleet-runner.yml', 'Setup Node')
        b = fp_for('unpinned-uses', 'fleet-runner.yml', 'Setup Node')
        self.assertEqual(a, b)

    def test_fp_for_uses_basename(self):
        # Full path and bare basename should produce the same fingerprint
        full = fp_for('artipacked', '.github/workflows/aeon.yml', 'top')
        bare = fp_for('artipacked', 'aeon.yml', 'top')
        self.assertEqual(full, bare)

    def test_fp_for_different_rules_differ(self):
        a = fp_for('artipacked', 'aeon.yml', 'top')
        b = fp_for('unpinned-uses', 'aeon.yml', 'top')
        self.assertNotEqual(a, b)

    def test_fp_trailer_spaces_become_underscores(self):
        with_space = fp_trailer('unpinned-uses', 'aeon.yml', 'Setup Node')
        with_underscore = fp_trailer('unpinned-uses', 'aeon.yml', 'Setup_Node')
        self.assertEqual(with_space, with_underscore)

    def test_fp_trailer_no_space_step_unchanged(self):
        a = fp_trailer('artipacked', 'aeon.yml', 'Checkout')
        b = fp_for('artipacked', 'aeon.yml', 'Checkout')
        self.assertEqual(a, b)


class TestCalibration(unittest.TestCase):

    def test_unpinned_uses_critical_downgraded_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        apply_unpinned_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertTrue(findings[0].get('calibrated'))

    def test_unpinned_uses_high_unchanged(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        apply_unpinned_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertNotIn('calibrated', findings[0])

    def test_unpinned_uses_medium_unchanged(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Medium'}]
        apply_unpinned_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_other_rule_critical_not_affected_by_unpinned_calibration(self):
        findings = [{'short_rule': 'artipacked', 'severity': 'Critical'}]
        apply_unpinned_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        apply_secrets_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_secrets_outside_env_medium_unchanged(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        apply_secrets_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_other_rule_high_not_affected_by_secrets_calibration(self):
        findings = [{'short_rule': 'artipacked', 'severity': 'High'}]
        apply_secrets_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')


class TestDeltaClassification(unittest.TestCase):

    def _make(self, rule, fname, line):
        return {'short_rule': rule, 'file': fname, 'line': line}

    def test_all_new_when_no_prior(self):
        findings = [
            self._make('artipacked', 'aeon.yml', 10),
            self._make('artipacked', 'aeon.yml', 20),
        ]
        classify_delta(findings, {})
        self.assertEqual([f['delta'] for f in findings], ['NEW', 'NEW'])

    def test_all_unchanged_when_prior_covers_all(self):
        findings = [
            self._make('artipacked', 'aeon.yml', 10),
            self._make('artipacked', 'aeon.yml', 20),
        ]
        classify_delta(findings, {('artipacked', 'aeon.yml'): 2})
        self.assertEqual([f['delta'] for f in findings], ['UNCHANGED', 'UNCHANGED'])

    def test_mix_unchanged_then_new_by_line_order(self):
        findings = [
            self._make('artipacked', 'aeon.yml', 30),
            self._make('artipacked', 'aeon.yml', 10),
            self._make('artipacked', 'aeon.yml', 20),
        ]
        classify_delta(findings, {('artipacked', 'aeon.yml'): 2})
        # sorted by line: 10 → UNCHANGED, 20 → UNCHANGED, 30 → NEW
        by_line = sorted(findings, key=lambda f: f['line'])
        self.assertEqual([f['delta'] for f in by_line], ['UNCHANGED', 'UNCHANGED', 'NEW'])

    def test_prior_exceeds_today_all_unchanged(self):
        findings = [self._make('artipacked', 'aeon.yml', 5)]
        classify_delta(findings, {('artipacked', 'aeon.yml'): 10})
        self.assertEqual(findings[0]['delta'], 'UNCHANGED')

    def test_different_rules_classified_independently(self):
        findings = [
            self._make('artipacked', 'aeon.yml', 1),
            self._make('unpinned-uses', 'aeon.yml', 2),
        ]
        # 1 prior artipacked, 0 prior unpinned-uses
        classify_delta(findings, {('artipacked', 'aeon.yml'): 1})
        deltas = {(f['short_rule'], f['line']): f['delta'] for f in findings}
        self.assertEqual(deltas[('artipacked', 1)], 'UNCHANGED')
        self.assertEqual(deltas[('unpinned-uses', 2)], 'NEW')

    def test_different_files_same_rule_classified_independently(self):
        findings = [
            self._make('artipacked', 'aeon.yml', 1),
            self._make('artipacked', 'messages.yml', 2),
        ]
        classify_delta(findings, {('artipacked', 'aeon.yml'): 1, ('artipacked', 'messages.yml'): 0})
        by_file = {f['file']: f['delta'] for f in findings}
        self.assertEqual(by_file['aeon.yml'], 'UNCHANGED')
        self.assertEqual(by_file['messages.yml'], 'NEW')

    def test_full_path_resolved_via_basename(self):
        findings = [self._make('artipacked', '.github/workflows/aeon.yml', 5)]
        classify_delta(findings, {('artipacked', 'aeon.yml'): 1})
        self.assertEqual(findings[0]['delta'], 'UNCHANGED')


if __name__ == '__main__':
    unittest.main()
