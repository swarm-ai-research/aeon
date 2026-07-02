"""
Tests for severity-mapping and calibration logic used by the workflow-security-audit pipeline.

These functions are extracted verbatim from classify.py, delta.py, and finalize.py so
they can be exercised in isolation without requiring the full pipeline data files.
"""

import hashlib
import os
import unittest


# ── from classify.py ─────────────────────────────────────────────────────────

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


# ── from delta.py ─────────────────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── calibration helpers (inline in delta.py / finalize.py) ───────────────────

def apply_delta_calibration(findings):
    """unpinned-uses error-level -> High (not Critical): policy-driven, not exploit-driven."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


def apply_finalize_calibration(findings):
    """secrets-outside-env High -> Medium: GitHub Environments hardening, not exploit."""
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium'
            )
    return findings


# ── tests ─────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    # Critical branch
    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_mixed_case_conf_normalised_to_critical(self):
        # Tool output may emit 'High' or 'HIGH'; .lower() must normalise before compare
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    # High branch — error without high confidence
    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_conf_key_is_high(self):
        # .get('confidence', '') falls back to '' — must not KeyError
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    # High branch — warning with high confidence
    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    # Medium branch — warning without high confidence
    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_low_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_empty_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_warning_missing_conf_key_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    # Low branch (fallthrough)
    def test_note_level_is_low_regardless_of_conf(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')
        self.assertEqual(our_severity({'level': 'note', 'confidence': ''}), 'Low')

    def test_unknown_level_falls_through_to_low(self):
        self.assertEqual(our_severity({'level': 'unknown', 'confidence': 'high'}), 'Low')
        self.assertEqual(our_severity({'level': '', 'confidence': 'high'}), 'Low')


class TestDeltaCalibration(unittest.TestCase):

    def test_unpinned_uses_critical_downgraded_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        apply_delta_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertTrue(findings[0].get('calibrated'))

    def test_unpinned_uses_high_not_modified(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        apply_delta_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertNotIn('calibrated', findings[0])

    def test_other_critical_rule_not_downgraded(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
        apply_delta_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')

    def test_calibration_does_not_affect_unrelated_rules(self):
        findings = [
            {'short_rule': 'unpinned-uses', 'severity': 'Critical'},
            {'short_rule': 'artipacked', 'severity': 'Critical'},
        ]
        apply_delta_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertEqual(findings[1]['severity'], 'Critical')  # untouched


class TestFinalizeCalibration(unittest.TestCase):

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_secrets_outside_env_medium_unchanged(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_secrets_outside_env_critical_unchanged(self):
        # Only High is downgraded; Critical is left alone (shouldn't appear in practice
        # but the guard must be strict: only `== 'High'`)
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Critical'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')

    def test_other_rule_high_unchanged(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'High'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')


class TestFpFor(unittest.TestCase):

    def test_deterministic(self):
        fp1 = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        fp2 = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        self.assertEqual(fp1, fp2)

    def test_uses_basename_only(self):
        fp_full = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'step')
        fp_base = fp_for('unpinned-uses', 'ci.yml', 'step')
        self.assertEqual(fp_full, fp_base)

    def test_output_is_16_lowercase_hex_chars(self):
        fp = fp_for('any-rule', 'file.yml', 'some step')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_differs_by_rule(self):
        fp1 = fp_for('rule-a', 'ci.yml', 'step')
        fp2 = fp_for('rule-b', 'ci.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_differs_by_file(self):
        fp1 = fp_for('rule', 'a.yml', 'step')
        fp2 = fp_for('rule', 'b.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_underscore_vs_space_in_step_produces_different_fingerprint(self):
        # delta.py normalises prior fingerprint steps from 'Setup_Node' -> 'Setup Node'
        # before lookup; this test documents why the normalisation is necessary.
        fp_under = fp_for('unpinned-uses', 'ci.yml', 'Setup_Node')
        fp_space = fp_for('unpinned-uses', 'ci.yml', 'Setup Node')
        self.assertNotEqual(fp_under, fp_space)


if __name__ == '__main__':
    unittest.main()
