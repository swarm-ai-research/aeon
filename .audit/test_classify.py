"""
Tests for severity-classification and fingerprint logic used by the
workflow-security-audit skill to process actionlint and zizmor output.

Run: python3 .audit/test_classify.py
"""

import hashlib
import os
import unittest


# ---------------------------------------------------------------------------
# Logic under test — inlined to avoid triggering classify.py's top-level file
# reads (classify.py calls open('.audit/parsed.json') at import time).
# Keep these in sync with .audit/classify.py and .audit/delta.py.
# ---------------------------------------------------------------------------

def our_severity(f):
    """Source: .audit/classify.py"""
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
    """Source: .audit/delta.py"""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def apply_unpinned_uses_calibration(findings):
    """Source: .audit/delta.py — unpinned-uses policy override."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


def apply_finalize_calibration(findings):
    """Source: .audit/finalize.py — secrets-outside-env downgrade."""
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)'
            )
    return findings


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestOurSeverity(unittest.TestCase):
    """Tests for every branch of the our_severity() classifier."""

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_uppercase_confidence_normalises_to_critical(self):
        # conf is lowercased before comparison — case variants must map correctly.
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_empty_confidence_is_high(self):
        # An empty string is not 'high', so the second branch fires.
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_confidence_key_defaults_to_high(self):
        # confidence key absent → get() returns '' → not 'high' → High
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_warning_missing_confidence_key_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_is_always_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')
        self.assertEqual(our_severity({'level': 'note', 'confidence': ''}), 'Low')

    def test_unknown_level_falls_through_to_low(self):
        self.assertEqual(our_severity({'level': 'info'}), 'Low')
        self.assertEqual(our_severity({'level': ''}), 'Low')


class TestFpFor(unittest.TestCase):
    """Tests for the fingerprint helper in delta.py."""

    def test_deterministic(self):
        a = fp_for('template-injection', '.github/workflows/ci.yml', 'Build')
        b = fp_for('template-injection', '.github/workflows/ci.yml', 'Build')
        self.assertEqual(a, b)

    def test_length_is_16(self):
        fp = fp_for('some-rule', 'some-file.yml', 'some step')
        self.assertEqual(len(fp), 16)

    def test_only_basename_used(self):
        # Two paths with the same basename must produce the same fingerprint.
        fp1 = fp_for('rule', '.github/workflows/deploy.yml', 'step')
        fp2 = fp_for('rule', 'deploy.yml', 'step')
        self.assertEqual(fp1, fp2)

    def test_different_rules_differ(self):
        fp1 = fp_for('rule-a', 'file.yml', 'step')
        fp2 = fp_for('rule-b', 'file.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_different_steps_differ(self):
        fp1 = fp_for('rule', 'file.yml', 'Setup Node')
        fp2 = fp_for('rule', 'file.yml', 'Build')
        self.assertNotEqual(fp1, fp2)


class TestCalibrationOverrides(unittest.TestCase):
    """Tests for the two policy-driven severity downgrades."""

    # --- delta.py: unpinned-uses Critical → High ---

    def test_unpinned_uses_critical_downgraded_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertTrue(result[0].get('calibrated'))

    def test_unpinned_uses_high_unchanged(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertNotIn('calibrated', result[0])

    def test_other_rules_critical_unchanged_by_unpinned_calibration(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Critical')

    # --- finalize.py: secrets-outside-env High → Medium ---

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')
        self.assertTrue(len(result[0].get('calibrated_notes', [])) > 0)

    def test_secrets_outside_env_critical_unchanged(self):
        # Only 'High' is downgraded; Critical is left alone.
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Critical'}]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Critical')

    def test_secrets_outside_env_medium_unchanged(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')

    def test_other_rules_high_unchanged_by_finalize_calibration(self):
        findings = [{'short_rule': 'artipacked', 'severity': 'High'}]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')


if __name__ == '__main__':
    unittest.main()
