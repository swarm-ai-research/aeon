"""
Unit tests for the pure-function logic in classify.py, delta.py, and finalize.py.

These scripts execute on import, so the functions under test are reimplemented
here verbatim. Tests cover edge cases that the scripts never exercised: confidence
case-insensitivity, missing-key fallback, basename stripping, calibration scoping.

Run with: python -m pytest .audit/test_logic.py  OR  python .audit/test_logic.py
"""

import hashlib
import os
import unittest


# ---------------------------------------------------------------------------
# Reimplemented pure functions (identical to production — changes here = bug)
# ---------------------------------------------------------------------------

def our_severity(f):
    """From classify.py — maps zizmor SARIF level+confidence to our severity."""
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
    """From delta.py — stable 16-char fingerprint for a finding."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def apply_unpinned_uses_calibration(findings):
    """From delta.py / delta2.py — unpinned-uses Critical → High (policy, not exploit)."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


def apply_secrets_calibration(findings):
    """From finalize.py — secrets-outside-env High → Medium (env-hardening, not RCE)."""
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

    # --- error level ---

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_confidence_uppercase_is_critical(self):
        # .lower() normalises; 'HIGH' must not fall through to the bare 'error' branch
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_high_confidence_mixed_case_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_confidence_is_high(self):
        # empty string != 'high', falls through to bare 'error' branch
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_confidence_key_is_high(self):
        # .get('confidence', '') returns '' — must not KeyError or become Critical
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    # --- warning level ---

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_high_confidence_uppercase_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_no_confidence_key_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    # --- note / unknown ---

    def test_note_high_confidence_is_low(self):
        # 'note' doesn't match error/warning branches — confidence is irrelevant
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_note_no_confidence_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({'level': '', 'confidence': 'high'}), 'Low')


class TestFpFor(unittest.TestCase):

    def test_returns_16_hex_chars(self):
        fp = fp_for('template-injection', '.github/workflows/foo.yml', 'Build')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_strips_directory_components(self):
        # delta.py uses os.path.basename — only the filename should matter
        fp1 = fp_for('rule', '.github/workflows/foo.yml', 'step')
        fp2 = fp_for('rule', 'foo.yml', 'step')
        self.assertEqual(fp1, fp2)

    def test_different_paths_same_basename_are_equal(self):
        fp1 = fp_for('rule', 'a/b/c/deploy.yml', 'Deploy')
        fp2 = fp_for('rule', 'x/y/deploy.yml', 'Deploy')
        self.assertEqual(fp1, fp2)

    def test_different_basenames_differ(self):
        fp1 = fp_for('rule', 'foo.yml', 'step')
        fp2 = fp_for('rule', 'bar.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_different_rules_differ(self):
        fp1 = fp_for('template-injection', 'foo.yml', 'step')
        fp2 = fp_for('unpinned-uses', 'foo.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_step_underscore_vs_space_differ(self):
        # delta.py normalises underscores to spaces when comparing against prior
        # fingerprints, but fp_for itself is case/whitespace-exact
        fp1 = fp_for('rule', 'foo.yml', 'Setup Node')
        fp2 = fp_for('rule', 'foo.yml', 'Setup_Node')
        self.assertNotEqual(fp1, fp2)

    def test_empty_step_does_not_raise(self):
        fp = fp_for('rule', 'foo.yml', '')
        self.assertEqual(len(fp), 16)

    def test_deterministic_across_calls(self):
        fp1 = fp_for('template-injection', 'deploy.yml', 'Run deploy')
        fp2 = fp_for('template-injection', 'deploy.yml', 'Run deploy')
        self.assertEqual(fp1, fp2)

    def test_unicode_step_name(self):
        # Should not crash with non-ASCII step names
        fp = fp_for('rule', 'foo.yml', 'Deploy 🚀')
        self.assertEqual(len(fp), 16)


class TestUnpinnedUsesCalibration(unittest.TestCase):

    def test_critical_downgraded_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')

    def test_downgraded_finding_gets_calibrated_flag(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        result = apply_unpinned_uses_calibration(findings)
        self.assertTrue(result[0].get('calibrated'))

    def test_high_stays_high_no_calibrated_flag(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertNotIn('calibrated', result[0])

    def test_other_rule_critical_unchanged(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Critical')

    def test_mixed_list_only_matching_downgraded(self):
        findings = [
            {'short_rule': 'unpinned-uses', 'severity': 'Critical'},
            {'short_rule': 'template-injection', 'severity': 'Critical'},
            {'short_rule': 'unpinned-uses', 'severity': 'High'},
        ]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')     # downgraded
        self.assertEqual(result[1]['severity'], 'Critical') # other rule untouched
        self.assertEqual(result[2]['severity'], 'High')     # already High, no change


class TestSecretsOutsideEnvCalibration(unittest.TestCase):

    def test_high_downgraded_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        result = apply_secrets_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')

    def test_calibrated_note_added(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        result = apply_secrets_calibration(findings)
        self.assertIn('calibrated_notes', result[0])
        self.assertIn('High->Medium', result[0]['calibrated_notes'][0])

    def test_medium_unchanged_no_note(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        result = apply_secrets_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')
        self.assertNotIn('calibrated_notes', result[0])

    def test_other_high_unchanged(self):
        findings = [{'short_rule': 'artipacked', 'severity': 'High'}]
        result = apply_secrets_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')

    def test_existing_calibrated_notes_extended_not_replaced(self):
        # setdefault means pre-existing notes are preserved
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High',
                     'calibrated_notes': ['prior note']}]
        result = apply_secrets_calibration(findings)
        self.assertEqual(len(result[0]['calibrated_notes']), 2)
        self.assertEqual(result[0]['calibrated_notes'][0], 'prior note')


if __name__ == '__main__':
    unittest.main()
