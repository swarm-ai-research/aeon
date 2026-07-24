"""Tests for audit classification and fingerprinting logic.

Covers our_severity() (classify.py / extract_steps.py) and fp_for() (delta.py)
plus the calibration overrides in delta.py and finalize.py. The scripts run at
module level so their functions are reproduced inline here.
"""
import hashlib
import os
import unittest


def our_severity(f):
    """Reproduced from classify.py / extract_steps.py."""
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
    """Reproduced from delta.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class TestOurSeverity(unittest.TestCase):
    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_confidence_case_insensitive(self):
        # .lower() is applied, so 'HIGH' and 'High' both map to Critical
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_missing_confidence_is_high(self):
        # Key absent — default '' != 'high', so falls to second error branch
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_is_low(self):
        # note-level findings land in Low regardless of confidence
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')
        self.assertEqual(our_severity({'level': '', 'confidence': 'high'}), 'Low')


class TestFpFor(unittest.TestCase):
    def test_returns_16_char_hex(self):
        result = fp_for('unpinned-uses', 'deploy.yml', 'Checkout')
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_strips_directory_prefix(self):
        # Both should produce the same fingerprint
        full_path = fp_for('unpinned-uses', '.github/workflows/deploy.yml', 'Checkout')
        basename_only = fp_for('unpinned-uses', 'deploy.yml', 'Checkout')
        self.assertEqual(full_path, basename_only)

    def test_same_basename_different_dirs_collide(self):
        # Known limitation: two workflows sharing a filename get the same fp
        a = fp_for('artipacked', 'team_a/ci.yml', 'Build')
        b = fp_for('artipacked', 'team_b/ci.yml', 'Build')
        self.assertEqual(a, b)

    def test_different_rules_differ(self):
        a = fp_for('artipacked', 'ci.yml', 'Checkout')
        b = fp_for('unpinned-uses', 'ci.yml', 'Checkout')
        self.assertNotEqual(a, b)

    def test_different_steps_differ(self):
        a = fp_for('artipacked', 'ci.yml', 'Checkout')
        b = fp_for('artipacked', 'ci.yml', 'Build')
        self.assertNotEqual(a, b)

    def test_deterministic(self):
        self.assertEqual(fp_for('r', 'f.yml', 's'), fp_for('r', 'f.yml', 's'))

    def test_empty_inputs(self):
        result = fp_for('', '', '')
        self.assertEqual(len(result), 16)


class TestDeltaCalibration(unittest.TestCase):
    """Covers the unpinned-uses Critical→High override in delta.py."""

    def _apply(self, findings):
        for f in findings:
            if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
                f['severity'] = 'High'
                f['calibrated'] = True
        return findings

    def test_unpinned_uses_critical_downgraded(self):
        f = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        self.assertEqual(self._apply(f)[0]['severity'], 'High')
        self.assertTrue(self._apply(f)[0].get('calibrated'))

    def test_unpinned_uses_high_unchanged(self):
        f = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        self.assertEqual(self._apply(f)[0]['severity'], 'High')
        self.assertNotIn('calibrated', self._apply(f)[0])

    def test_unpinned_uses_medium_unchanged(self):
        f = [{'short_rule': 'unpinned-uses', 'severity': 'Medium'}]
        self.assertEqual(self._apply(f)[0]['severity'], 'Medium')

    def test_other_rules_not_touched(self):
        f = [{'short_rule': 'artipacked', 'severity': 'Critical'}]
        self.assertEqual(self._apply(f)[0]['severity'], 'Critical')
        self.assertNotIn('calibrated', self._apply(f)[0])

    def test_multiple_findings_only_target_affected(self):
        findings = [
            {'short_rule': 'unpinned-uses', 'severity': 'Critical'},
            {'short_rule': 'artipacked', 'severity': 'Critical'},
        ]
        result = self._apply(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertEqual(result[1]['severity'], 'Critical')


class TestFinalizeCalibration(unittest.TestCase):
    """Covers the secrets-outside-env High→Medium override in finalize.py."""

    def _apply(self, findings):
        for f in findings:
            if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
                f['severity'] = 'Medium'
                f.setdefault('calibrated_notes', []).append(
                    'secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)'
                )
        return findings

    def test_secrets_outside_env_high_downgraded(self):
        f = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        result = self._apply(f)
        self.assertEqual(result[0]['severity'], 'Medium')
        self.assertEqual(len(result[0]['calibrated_notes']), 1)

    def test_secrets_outside_env_medium_unchanged(self):
        f = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        result = self._apply(f)
        self.assertEqual(result[0]['severity'], 'Medium')
        self.assertNotIn('calibrated_notes', result[0])

    def test_secrets_outside_env_critical_unchanged(self):
        # Only 'High' is in scope for the finalize downgrade
        f = [{'short_rule': 'secrets-outside-env', 'severity': 'Critical'}]
        result = self._apply(f)
        self.assertEqual(result[0]['severity'], 'Critical')

    def test_other_rules_high_not_touched(self):
        f = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        result = self._apply(f)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertNotIn('calibrated_notes', result[0])


if __name__ == '__main__':
    unittest.main()
