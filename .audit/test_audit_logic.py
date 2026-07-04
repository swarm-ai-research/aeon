"""Unit tests for pure functions embedded in the .audit/ pipeline scripts.

Run with: python -m pytest .audit/test_audit_logic.py -v
      or: python .audit/test_audit_logic.py
"""

import hashlib
import os
import unittest


# ── Functions under test ────────────────────────────────────────────────────
# These are copied verbatim from the audit pipeline scripts so that they can
# be tested without importing the scripts (which run file I/O at module level).
# Each block notes its source file.

# Source: classify.py / extract_steps.py  (same logic in both)
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


# Source: delta.py — fp_for uses step as-is (spaces preserved)
def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# Source: gen_trailer.py — fp normalises spaces → underscores in step
def fp_gen_trailer(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# Source: delta2.py
def short_rule(s):
    return s.split('/')[-1]


# Source: delta.py and delta2.py — is_hex_fp detects individual fingerprints
def is_hex_fp(token):
    return len(token) == 16 and all(c in '0123456789abcdef' for c in token)


# Source: delta.py — calibration override for unpinned-uses
def apply_unpinned_uses_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


# Source: finalize.py — calibration override for secrets-outside-env
def apply_secrets_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)'
            )
    return findings


# ── Tests ───────────────────────────────────────────────────────────────────

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
        # confidence key absent → get() returns '' → not 'high' → High branch
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_is_low_regardless_of_confidence(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'low'}), 'Low')
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info'}), 'Low')
        self.assertEqual(our_severity({'level': ''}), 'Low')


class TestFingerprintFunctions(unittest.TestCase):

    def test_fp_for_is_deterministic(self):
        a = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Checkout')
        b = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Checkout')
        self.assertEqual(a, b)

    def test_fp_for_uses_basename_only(self):
        # Full path and basename-only should produce the same fingerprint
        full = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Checkout')
        base = fp_for('unpinned-uses', 'ci.yml', 'Checkout')
        self.assertEqual(full, base)

    def test_fp_for_output_is_16_hex_chars(self):
        result = fp_for('template-injection', 'deploy.yml', 'Run tests')
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_fp_for_space_vs_underscore_differ(self):
        # delta.py preserves spaces; gen_trailer.py normalises to underscores.
        # These intentionally differ because they serve different purposes.
        with_space = fp_for('rule', 'workflow.yml', 'Setup Node')
        with_under = fp_for('rule', 'workflow.yml', 'Setup_Node')
        self.assertNotEqual(with_space, with_under)

    def test_fp_gen_trailer_normalises_spaces_to_underscores(self):
        # gen_trailer's fp() converts spaces → underscores before hashing
        step_space = fp_gen_trailer('rule', 'workflow.yml', 'Setup Node')
        step_under = fp_gen_trailer('rule', 'workflow.yml', 'Setup_Node')
        self.assertEqual(step_space, step_under)

    def test_fp_gen_trailer_uses_basename(self):
        full = fp_gen_trailer('rule', '.github/workflows/ci.yml', 'step')
        base = fp_gen_trailer('rule', 'ci.yml', 'step')
        self.assertEqual(full, base)

    def test_different_rules_produce_different_fps(self):
        a = fp_for('rule-a', 'ci.yml', 'step')
        b = fp_for('rule-b', 'ci.yml', 'step')
        self.assertNotEqual(a, b)

    def test_different_steps_produce_different_fps(self):
        a = fp_for('rule', 'ci.yml', 'step-a')
        b = fp_for('rule', 'ci.yml', 'step-b')
        self.assertNotEqual(a, b)


class TestShortRule(unittest.TestCase):

    def test_strips_namespace_prefix(self):
        self.assertEqual(short_rule('zizmor/template-injection'), 'template-injection')

    def test_rule_without_slash_unchanged(self):
        self.assertEqual(short_rule('unpinned-uses'), 'unpinned-uses')

    def test_multiple_slashes_takes_last_segment(self):
        self.assertEqual(short_rule('a/b/c'), 'c')

    def test_empty_string(self):
        self.assertEqual(short_rule(''), '')


class TestIsHexFp(unittest.TestCase):

    def test_valid_16_char_hex_is_fp(self):
        self.assertTrue(is_hex_fp('abcdef0123456789'))

    def test_rule_name_is_not_fp(self):
        self.assertFalse(is_hex_fp('secrets-outside-env'))

    def test_15_char_hex_is_not_fp(self):
        self.assertFalse(is_hex_fp('abcdef012345678'))

    def test_17_char_hex_is_not_fp(self):
        self.assertFalse(is_hex_fp('abcdef01234567890'))

    def test_16_char_with_non_hex_char_is_not_fp(self):
        # 'g' is not a valid hex character
        self.assertFalse(is_hex_fp('abcdef012345678g'))

    def test_uppercase_hex_is_not_fp(self):
        # The check requires lowercase hex only (matches sha256.hexdigest() output)
        self.assertFalse(is_hex_fp('ABCDEF0123456789'))

    def test_empty_string_is_not_fp(self):
        self.assertFalse(is_hex_fp(''))


class TestCalibrationOverrides(unittest.TestCase):

    def test_unpinned_uses_critical_downgraded_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertTrue(result[0].get('calibrated'))

    def test_unpinned_uses_high_not_changed(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertNotIn('calibrated', result[0])

    def test_other_rule_critical_not_downgraded(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Critical')

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        result = apply_secrets_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')
        self.assertTrue(len(result[0].get('calibrated_notes', [])) > 0)

    def test_secrets_outside_env_medium_not_changed(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        result = apply_secrets_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')

    def test_other_rule_high_not_downgraded_by_secrets_calibration(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        result = apply_secrets_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')

    def test_calibrations_applied_independently(self):
        findings = [
            {'short_rule': 'unpinned-uses', 'severity': 'Critical'},
            {'short_rule': 'secrets-outside-env', 'severity': 'High'},
            {'short_rule': 'template-injection', 'severity': 'Critical'},
        ]
        apply_unpinned_uses_calibration(findings)
        apply_secrets_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')    # unpinned-uses downgraded
        self.assertEqual(findings[1]['severity'], 'Medium')  # secrets-outside-env downgraded
        self.assertEqual(findings[2]['severity'], 'Critical')  # template-injection unchanged


if __name__ == '__main__':
    unittest.main()
