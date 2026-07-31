"""
Unit tests for pure logic in .audit/ scripts.
Run: python .audit/test_classify.py
"""

import hashlib
import os
import unittest


# ── Extracted from classify.py / extract_steps.py ────────────────────────────

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


# ── Extracted from delta.py ───────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def is_hex_fp(key):
    return len(key) == 16 and all(c in '0123456789abcdef' for c in key)


# ── Extracted from delta.py / finalize.py ────────────────────────────────────

def apply_calibration(findings):
    """unpinned-uses Critical → High (policy uplift, not exploit-driven)."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


def apply_finalize_calibration(findings):
    """secrets-outside-env High → Medium (GitHub Environments hardening tier)."""
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
    return findings


# ─────────────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_low_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_missing_conf_is_high(self):
        # No 'confidence' key → defaults to '' → not 'high' → second branch
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_conf_is_medium(self):
        # 'medium' is not 'high' → falls to the plain warning branch
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_empty_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_note_high_conf_is_low(self):
        # 'note' level never matches error/warning branches → Low (else clause)
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_note_no_conf_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': ''}), 'Low')

    def test_confidence_uppercased_normalised(self):
        # confidence is .lower()'d before comparison; 'HIGH' → 'high' → Critical
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_unknown_level_is_low(self):
        # Any unrecognised level (e.g. 'info') falls through to Low
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')


class TestFpFor(unittest.TestCase):

    def test_returns_16_char_lowercase_hex(self):
        fp = fp_for('artipacked', '.github/workflows/ci.yml', 'Checkout')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_deterministic(self):
        self.assertEqual(
            fp_for('artipacked', 'ci.yml', 'Checkout'),
            fp_for('artipacked', 'ci.yml', 'Checkout'),
        )

    def test_basename_only_used(self):
        # Full path and plain basename produce the same fingerprint
        fp1 = fp_for('artipacked', '.github/workflows/ci.yml', 'Checkout')
        fp2 = fp_for('artipacked', 'ci.yml', 'Checkout')
        self.assertEqual(fp1, fp2)

    def test_different_steps_differ(self):
        fp1 = fp_for('artipacked', 'ci.yml', 'Checkout')
        fp2 = fp_for('artipacked', 'ci.yml', 'Setup Node')
        self.assertNotEqual(fp1, fp2)

    def test_underscore_vs_space_differ(self):
        # delta.py normalises underscores→spaces before calling fp_for, but the
        # function itself does no normalisation — raw difference produces distinct fps.
        fp1 = fp_for('artipacked', 'ci.yml', 'Setup_Node')
        fp2 = fp_for('artipacked', 'ci.yml', 'Setup Node')
        self.assertNotEqual(fp1, fp2)

    def test_different_rules_differ(self):
        fp1 = fp_for('artipacked', 'ci.yml', 'Checkout')
        fp2 = fp_for('unpinned-uses', 'ci.yml', 'Checkout')
        self.assertNotEqual(fp1, fp2)

    def test_different_files_differ(self):
        fp1 = fp_for('artipacked', 'ci.yml', 'Checkout')
        fp2 = fp_for('artipacked', 'deploy.yml', 'Checkout')
        self.assertNotEqual(fp1, fp2)


class TestIsHexFp(unittest.TestCase):

    def test_valid_16_char_hex(self):
        self.assertTrue(is_hex_fp('abcdef0123456789'))

    def test_too_short_is_false(self):
        self.assertFalse(is_hex_fp('abcdef012345678'))   # 15 chars

    def test_too_long_is_false(self):
        self.assertFalse(is_hex_fp('abcdef01234567890'))  # 17 chars

    def test_uppercase_hex_chars_are_rejected(self):
        # Fingerprints are always lowercase hex; uppercase is not in the allowed set
        self.assertFalse(is_hex_fp('ABCDEF0123456789'))

    def test_rule_name_is_not_hex(self):
        self.assertFalse(is_hex_fp('artipacked'))

    def test_aggregate_rule_key_is_not_hex(self):
        self.assertFalse(is_hex_fp('secrets-outside-env'))

    def test_mixed_valid_invalid_chars(self):
        # 'g' is not a hex digit
        self.assertFalse(is_hex_fp('abcdef012345678g'))


class TestCalibrationOverrides(unittest.TestCase):

    def test_unpinned_uses_critical_downgraded_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertTrue(findings[0].get('calibrated'))

    def test_other_rules_not_affected_by_unpinned_calibration(self):
        findings = [{'short_rule': 'artipacked', 'severity': 'Critical'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')
        self.assertNotIn('calibrated', findings[0])

    def test_unpinned_uses_already_high_unchanged(self):
        # Calibration only fires on Critical; High stays High, no 'calibrated' flag
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertNotIn('calibrated', findings[0])

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_secrets_outside_env_medium_unchanged(self):
        # Calibration only fires on High; Medium stays Medium
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_other_rules_not_affected_by_finalize_calibration(self):
        findings = [{'short_rule': 'artipacked', 'severity': 'High'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')


if __name__ == '__main__':
    unittest.main(verbosity=2)
