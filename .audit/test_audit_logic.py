"""Tests for pure logic extracted from .audit/ processing scripts.

Run: python3 .audit/test_audit_logic.py
"""

import hashlib
import os
import unittest


# --- Extracted from classify.py / extract_steps.py ---
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


# --- Extracted from delta.py ---
def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# --- Calibration: unpinned-uses error → High (from delta.py / delta3.py) ---
def apply_unpinned_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


# --- Calibration: secrets-outside-env High → Medium (from finalize.py) ---
def apply_finalize_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)'
            )
    return findings


# --- Delta assignment (from delta3.py) ---
def assign_delta(findings, prior_counts):
    """Tag each finding NEW or UNCHANGED.

    For each (rule, basename) pair, the first prior_count findings
    (sorted by line) are UNCHANGED; the rest are NEW.
    """
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


class TestOurSeverity(unittest.TestCase):
    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_confidence_case_insensitive(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_no_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_confidence_key_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_no_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_note_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info', 'confidence': ''}), 'Low')


class TestFpFor(unittest.TestCase):
    def test_returns_16_hex_chars(self):
        fp = fp_for('template-injection', 'aeon.yml', 'Setup Node')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_strips_directory_prefix(self):
        fp_base = fp_for('template-injection', 'aeon.yml', 'Setup Node')
        fp_path = fp_for('template-injection', '.github/workflows/aeon.yml', 'Setup Node')
        self.assertEqual(fp_base, fp_path)

    def test_different_rules_produce_different_fps(self):
        fp1 = fp_for('template-injection', 'aeon.yml', 'step')
        fp2 = fp_for('unpinned-uses', 'aeon.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_different_steps_produce_different_fps(self):
        fp1 = fp_for('template-injection', 'aeon.yml', 'step A')
        fp2 = fp_for('template-injection', 'aeon.yml', 'step B')
        self.assertNotEqual(fp1, fp2)

    def test_different_files_produce_different_fps(self):
        fp1 = fp_for('rule', 'aeon.yml', 'step')
        fp2 = fp_for('rule', 'messages.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_stable_across_calls(self):
        fp1 = fp_for('rule', 'file.yml', 'step')
        fp2 = fp_for('rule', 'file.yml', 'step')
        self.assertEqual(fp1, fp2)


class TestUnpinnedCalibration(unittest.TestCase):
    def test_unpinned_critical_downgraded_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        result = apply_unpinned_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertTrue(result[0].get('calibrated'))

    def test_unpinned_high_not_touched(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        result = apply_unpinned_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertNotIn('calibrated', result[0])

    def test_other_rule_critical_not_downgraded(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
        result = apply_unpinned_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Critical')

    def test_empty_findings(self):
        self.assertEqual(apply_unpinned_calibration([]), [])

    def test_mixed_findings_only_matching_rule_changed(self):
        findings = [
            {'short_rule': 'unpinned-uses', 'severity': 'Critical'},
            {'short_rule': 'template-injection', 'severity': 'Critical'},
        ]
        result = apply_unpinned_calibration(findings)
        by_rule = {f['short_rule']: f['severity'] for f in result}
        self.assertEqual(by_rule['unpinned-uses'], 'High')
        self.assertEqual(by_rule['template-injection'], 'Critical')


class TestFinalizeCalibration(unittest.TestCase):
    def test_secrets_outside_env_high_downgraded_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')
        self.assertIn('calibrated_notes', result[0])
        self.assertEqual(len(result[0]['calibrated_notes']), 1)

    def test_secrets_outside_env_medium_not_touched(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')
        self.assertNotIn('calibrated_notes', result[0])

    def test_other_rule_high_not_downgraded(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertNotIn('calibrated_notes', result[0])

    def test_multiple_high_secrets_findings_all_downgraded(self):
        findings = [
            {'short_rule': 'secrets-outside-env', 'severity': 'High'},
            {'short_rule': 'secrets-outside-env', 'severity': 'High'},
        ]
        result = apply_finalize_calibration(findings)
        self.assertTrue(all(f['severity'] == 'Medium' for f in result))


class TestAssignDelta(unittest.TestCase):
    def _make(self, rule, fname, line):
        return {'short_rule': rule, 'file': fname, 'line': line}

    def test_no_prior_all_new(self):
        findings = [self._make('rule', 'f.yml', 10), self._make('rule', 'f.yml', 20)]
        result = assign_delta(findings, {})
        self.assertTrue(all(f['delta'] == 'NEW' for f in result))

    def test_prior_count_marks_first_n_as_unchanged(self):
        findings = [
            self._make('template-injection', 'aeon.yml', 10),
            self._make('template-injection', 'aeon.yml', 20),
            self._make('template-injection', 'aeon.yml', 30),
        ]
        result = assign_delta(findings, {('template-injection', 'aeon.yml'): 2})
        sorted_f = sorted(result, key=lambda x: x['line'])
        self.assertEqual(sorted_f[0]['delta'], 'UNCHANGED')
        self.assertEqual(sorted_f[1]['delta'], 'UNCHANGED')
        self.assertEqual(sorted_f[2]['delta'], 'NEW')

    def test_prior_exceeds_current_all_unchanged(self):
        findings = [self._make('rule', 'f.yml', 1)]
        result = assign_delta(findings, {('rule', 'f.yml'): 5})
        self.assertEqual(result[0]['delta'], 'UNCHANGED')

    def test_different_rules_handled_independently(self):
        findings = [self._make('rule-a', 'f.yml', 1), self._make('rule-b', 'f.yml', 2)]
        prior = {('rule-a', 'f.yml'): 1, ('rule-b', 'f.yml'): 0}
        result = assign_delta(findings, prior)
        by_rule = {f['short_rule']: f['delta'] for f in result}
        self.assertEqual(by_rule['rule-a'], 'UNCHANGED')
        self.assertEqual(by_rule['rule-b'], 'NEW')

    def test_directory_prefix_stripped_for_matching(self):
        findings = [
            self._make('rule', '.github/workflows/aeon.yml', 10),
            self._make('rule', '.github/workflows/aeon.yml', 20),
        ]
        result = assign_delta(findings, {('rule', 'aeon.yml'): 1})
        sorted_f = sorted(result, key=lambda x: x['line'])
        self.assertEqual(sorted_f[0]['delta'], 'UNCHANGED')
        self.assertEqual(sorted_f[1]['delta'], 'NEW')

    def test_empty_findings(self):
        self.assertEqual(assign_delta([], {}), [])


if __name__ == '__main__':
    unittest.main()
