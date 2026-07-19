"""
Unit tests for pure utility functions in the .audit/ pipeline scripts.

Run with: python -m pytest .audit/test_utils.py
      or: python -m unittest .audit.test_utils
"""

import hashlib
import os
import unittest
from collections import Counter


# ── our_severity ────────────────────────────────────────────────────────────
# Copied verbatim from classify.py / extract_steps.py (both define this).

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


# ── fp_for ───────────────────────────────────────────────────────────────────
# Copied verbatim from delta.py.

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── classify_shellcheck_code ─────────────────────────────────────────────────
# Logic extracted from summarize_al.py: first-match priority, else 'other'.

_SHELLCHECK_PRIORITY = ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']

def classify_shellcheck_code(msg):
    for code in _SHELLCHECK_PRIORITY:
        if code in msg:
            return code
    return 'other'


# ── apply_finalize_calibration ───────────────────────────────────────────────
# Logic extracted from finalize.py: downgrade secrets-outside-env High→Medium.

def apply_finalize_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium'
            )
    return findings


# ── sarif_severity_prop ───────────────────────────────────────────────────────
# Logic extracted from parse_sarif.py: property cascade for severity.

def sarif_severity_prop(props):
    return (
        props.get('problem.severity')
        or props.get('zizmor/severity')
        or props.get('security-severity', '')
    )


# ─────────────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_conf_case_insensitive(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_no_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_no_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info'}), 'Low')


class TestFpFor(unittest.TestCase):

    def test_returns_16_hex_chars(self):
        result = fp_for('unpinned-uses', 'aeon.yml', 'Checkout')
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_basename_is_used_not_full_path(self):
        full = fp_for('rule', '.github/workflows/aeon.yml', 'step')
        base = fp_for('rule', 'aeon.yml', 'step')
        self.assertEqual(full, base)

    def test_different_rules_differ(self):
        a = fp_for('rule-a', 'aeon.yml', 'step')
        b = fp_for('rule-b', 'aeon.yml', 'step')
        self.assertNotEqual(a, b)

    def test_different_steps_differ(self):
        a = fp_for('rule', 'aeon.yml', 'Setup Node')
        b = fp_for('rule', 'aeon.yml', 'Setup_Node')
        self.assertNotEqual(a, b)

    def test_deterministic(self):
        self.assertEqual(
            fp_for('unpinned-uses', 'aeon.yml', 'Checkout'),
            fp_for('unpinned-uses', 'aeon.yml', 'Checkout'),
        )


class TestClassifyShellcheckCode(unittest.TestCase):

    def test_sc2086_detected(self):
        self.assertEqual(classify_shellcheck_code('SC2086 double quote'), 'SC2086')

    def test_sc2046_detected(self):
        self.assertEqual(classify_shellcheck_code('SC2046 word splitting'), 'SC2046')

    def test_first_priority_wins(self):
        # SC2086 comes before SC2046 in priority list
        self.assertEqual(classify_shellcheck_code('SC2086 and SC2046 both'), 'SC2086')

    def test_unknown_code_returns_other(self):
        self.assertEqual(classify_shellcheck_code('SC9999 unknown'), 'other')

    def test_empty_message_returns_other(self):
        self.assertEqual(classify_shellcheck_code(''), 'other')

    def test_sc2034_detected(self):
        self.assertEqual(classify_shellcheck_code('SC2034 variable unused'), 'SC2034')


class TestApplyFinalizeCalibration(unittest.TestCase):

    def test_secrets_outside_env_high_downgraded(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_calibrated_notes_added(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        apply_finalize_calibration(findings)
        self.assertIn('calibrated_notes', findings[0])

    def test_secrets_outside_env_medium_unchanged(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')
        self.assertNotIn('calibrated_notes', findings[0])

    def test_secrets_outside_env_critical_unchanged(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Critical'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')

    def test_other_rule_high_unchanged(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')

    def test_mixed_findings(self):
        findings = [
            {'short_rule': 'secrets-outside-env', 'severity': 'High'},
            {'short_rule': 'unpinned-uses', 'severity': 'High'},
            {'short_rule': 'secrets-outside-env', 'severity': 'Medium'},
        ]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')
        self.assertEqual(findings[1]['severity'], 'High')
        self.assertEqual(findings[2]['severity'], 'Medium')


class TestSarifSeverityProp(unittest.TestCase):

    def test_problem_severity_wins(self):
        props = {
            'problem.severity': 'high',
            'zizmor/severity': 'medium',
            'security-severity': 'low',
        }
        self.assertEqual(sarif_severity_prop(props), 'high')

    def test_falls_through_to_zizmor_severity(self):
        props = {'zizmor/severity': 'medium', 'security-severity': 'low'}
        self.assertEqual(sarif_severity_prop(props), 'medium')

    def test_falls_through_to_security_severity(self):
        props = {'security-severity': 'low'}
        self.assertEqual(sarif_severity_prop(props), 'low')

    def test_empty_when_all_absent(self):
        self.assertEqual(sarif_severity_prop({}), '')

    def test_skips_falsy_problem_severity(self):
        # An empty string is falsy — should fall through
        props = {'problem.severity': '', 'zizmor/severity': 'medium'}
        self.assertEqual(sarif_severity_prop(props), 'medium')


if __name__ == '__main__':
    unittest.main()
