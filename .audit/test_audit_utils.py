"""
Tests for pure logic extracted from the audit pipeline scripts
(classify.py, extract_steps.py, gen_trailer.py, delta.py, finalize.py).

Run with: python -m pytest .audit/test_audit_utils.py
      or: python .audit/test_audit_utils.py
"""

import hashlib
import os
import unittest


# ── Replicate the shared severity function (classify.py / extract_steps.py) ──

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


# ── Replicate fingerprint helpers from gen_trailer.py / delta.py ──

def fp_trailer(rule, fname, step):
    """gen_trailer.py uses spaces-to-underscores in the step."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def fp_delta(rule, fname, step):
    """delta.py fp_for: no space replacement in the hash input."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Replicate calibration logic ──

def apply_delta_calibration(findings):
    """delta.py: unpinned-uses Critical → High."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


def apply_finalize_calibration(findings):
    """finalize.py: secrets-outside-env High → Medium."""
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append('downgraded')
    return findings


# ─────────────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    # Happy-path branches
    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_conf_case_insensitive(self):
        # confidence is lowercased before comparison; 'High' must still map to Critical
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_conf_is_high(self):
        # No 'confidence' key at all — default '' is used
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_empty_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_warning_missing_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    # Edge-case levels that fall through to Low
    def test_note_level_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_note_level_no_conf_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_none_level_is_low(self):
        self.assertEqual(our_severity({'level': 'none'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({'level': ''}), 'Low')


class TestFingerprintTrailer(unittest.TestCase):

    def test_produces_16_hex_chars(self):
        result = fp_trailer('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_deterministic(self):
        a = fp_trailer('template-injection', 'workflows/build.yml', 'Run tests')
        b = fp_trailer('template-injection', 'workflows/build.yml', 'Run tests')
        self.assertEqual(a, b)

    def test_spaces_converted_to_underscores(self):
        # 'Setup Node' and 'Setup_Node' must produce the same fingerprint
        fp_spaces = fp_trailer('rule', 'file.yml', 'Setup Node')
        fp_underscores = fp_trailer('rule', 'file.yml', 'Setup_Node')
        # trailer converts spaces → underscores, so both hash inputs are identical
        self.assertEqual(fp_spaces, fp_underscores)

    def test_basename_extraction(self):
        fp_long = fp_trailer('rule', '.github/workflows/ci.yml', 'step')
        fp_base = fp_trailer('rule', 'ci.yml', 'step')
        self.assertEqual(fp_long, fp_base)

    def test_different_rules_differ(self):
        a = fp_trailer('unpinned-uses', 'ci.yml', 'step')
        b = fp_trailer('template-injection', 'ci.yml', 'step')
        self.assertNotEqual(a, b)

    def test_different_files_differ(self):
        a = fp_trailer('rule', 'ci.yml', 'step')
        b = fp_trailer('rule', 'deploy.yml', 'step')
        self.assertNotEqual(a, b)

    def test_different_steps_differ(self):
        a = fp_trailer('rule', 'ci.yml', 'Build')
        b = fp_trailer('rule', 'ci.yml', 'Test')
        self.assertNotEqual(a, b)


class TestFingerprintDelta(unittest.TestCase):
    """delta.py does NOT replace spaces with underscores in the hash input."""

    def test_spaces_and_underscores_differ(self):
        fp_space = fp_delta('rule', 'ci.yml', 'Setup Node')
        fp_under = fp_delta('rule', 'ci.yml', 'Setup_Node')
        self.assertNotEqual(fp_space, fp_under)

    def test_trailer_and_delta_differ_for_spaced_step(self):
        # gen_trailer replaces spaces; delta does not — the two helpers must diverge
        step = 'Run tests'
        self.assertNotEqual(fp_trailer('rule', 'f.yml', step), fp_delta('rule', 'f.yml', step))

    def test_trailer_and_delta_agree_for_underscore_step(self):
        # When there are no spaces, both helpers should produce the same hash
        step = 'Run_tests'
        self.assertEqual(fp_trailer('rule', 'f.yml', step), fp_delta('rule', 'f.yml', step))


class TestDeltaCalibration(unittest.TestCase):

    def test_unpinned_uses_critical_downgraded(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        apply_delta_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertTrue(findings[0].get('calibrated'))

    def test_unpinned_uses_high_unchanged(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        apply_delta_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertNotIn('calibrated', findings[0])

    def test_other_rule_critical_unchanged(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
        apply_delta_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')

    def test_mixed_findings(self):
        findings = [
            {'short_rule': 'unpinned-uses', 'severity': 'Critical'},
            {'short_rule': 'unpinned-uses', 'severity': 'High'},
            {'short_rule': 'template-injection', 'severity': 'Critical'},
        ]
        apply_delta_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')   # downgraded
        self.assertEqual(findings[1]['severity'], 'High')   # unchanged
        self.assertEqual(findings[2]['severity'], 'Critical')  # unaffected


class TestFinalizeCalibration(unittest.TestCase):

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')
        self.assertIn('calibrated_notes', findings[0])

    def test_secrets_outside_env_medium_unchanged(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')
        self.assertNotIn('calibrated_notes', findings[0])

    def test_other_rule_high_unchanged(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'High'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')


if __name__ == '__main__':
    unittest.main()
