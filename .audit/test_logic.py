"""
Unit tests for pure logic extracted from the .audit/ processing scripts.

Run with: python -m unittest .audit/test_logic.py
      or: python .audit/test_logic.py
"""

import hashlib
import os
import unittest


# ---------------------------------------------------------------------------
# Logic extracted from classify.py
# ---------------------------------------------------------------------------

def our_severity(f):
    """Severity mapping from classify.py — must stay in sync."""
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


def short_rule(rule_id):
    """Extract the short rule name used in classify.py."""
    return rule_id.split('/')[-1]


# ---------------------------------------------------------------------------
# Logic extracted from delta.py
# ---------------------------------------------------------------------------

def fp_for(rule, fname, step):
    """Fingerprint function from delta.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Logic extracted from summarize_al.py
# ---------------------------------------------------------------------------

SHELLCHECK_CODES = ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']


def categorize_al_message(msg):
    """Return the first matching ShellCheck code, or 'other'."""
    for code in SHELLCHECK_CODES:
        if code in msg:
            return code
    return 'other'


def is_high_candidate(msg):
    """Return True when a message references SC2086/SC2046 together with a github.* ref."""
    return ('SC2086' in msg or 'SC2046' in msg) and 'github.' in msg.lower()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestOurSeverity(unittest.TestCase):

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_conf_case_insensitive(self):
        # confidence is lowercased inside our_severity
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_low_conf_is_high_not_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_missing_conf_is_high(self):
        # confidence key absent entirely
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_conf_is_medium(self):
        # low confidence warning must NOT return 'Low' — it returns 'Medium'
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_no_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info'}), 'Low')


class TestShortRule(unittest.TestCase):

    def test_namespaced_rule(self):
        self.assertEqual(short_rule('zizmor/unpinned-uses'), 'unpinned-uses')

    def test_no_namespace(self):
        self.assertEqual(short_rule('unpinned-uses'), 'unpinned-uses')

    def test_multi_segment(self):
        self.assertEqual(short_rule('a/b/c'), 'c')


class TestFingerprintFor(unittest.TestCase):

    def test_deterministic(self):
        self.assertEqual(
            fp_for('unpinned-uses', 'ci.yml', 'Checkout'),
            fp_for('unpinned-uses', 'ci.yml', 'Checkout'),
        )

    def test_length_is_16(self):
        fp = fp_for('unpinned-uses', 'ci.yml', 'Checkout')
        self.assertEqual(len(fp), 16)

    def test_different_rule_gives_different_fp(self):
        fp1 = fp_for('unpinned-uses', 'ci.yml', 'Checkout')
        fp2 = fp_for('secrets-outside-env', 'ci.yml', 'Checkout')
        self.assertNotEqual(fp1, fp2)

    def test_basename_stripped(self):
        # Only the basename of the file path is used
        fp_full = fp_for('rule', '.github/workflows/ci.yml', 'step')
        fp_base = fp_for('rule', 'ci.yml', 'step')
        self.assertEqual(fp_full, fp_base)

    def test_different_file_gives_different_fp(self):
        fp1 = fp_for('rule', 'ci.yml', 'step')
        fp2 = fp_for('rule', 'deploy.yml', 'step')
        self.assertNotEqual(fp1, fp2)


class TestCategorizeAlMessage(unittest.TestCase):

    def test_sc2086_only(self):
        self.assertEqual(categorize_al_message('shellcheck warning SC2086: word splitting'), 'SC2086')

    def test_sc2046_only(self):
        self.assertEqual(categorize_al_message('SC2046 found'), 'SC2046')

    def test_no_match_returns_other(self):
        self.assertEqual(categorize_al_message('unrelated message'), 'other')

    def test_first_match_wins_over_later_code(self):
        # SC2086 appears before SC2046 in the priority list;
        # a message containing both must be counted under SC2086.
        msg = 'SC2086 unquoted and SC2046 eval'
        self.assertEqual(categorize_al_message(msg), 'SC2086')

    def test_sc2034_last_in_list(self):
        self.assertEqual(categorize_al_message('SC2034 unused variable'), 'SC2034')

    def test_empty_message(self):
        self.assertEqual(categorize_al_message(''), 'other')


class TestIsHighCandidate(unittest.TestCase):

    def test_sc2086_with_github_ref(self):
        self.assertTrue(is_high_candidate('SC2086: ${{github.event.inputs.branch}}'))

    def test_sc2046_with_github_ref(self):
        self.assertTrue(is_high_candidate('SC2046 github.sha unquoted'))

    def test_sc2086_without_github_ref(self):
        self.assertFalse(is_high_candidate('SC2086: $MY_VAR'))

    def test_github_ref_without_sc_code(self):
        self.assertFalse(is_high_candidate('github.event.inputs found'))

    def test_github_uppercase_still_matches(self):
        # msg.lower() is used, so uppercase GITHUB. also triggers
        self.assertTrue(is_high_candidate('SC2086 in GITHUB.ACTOR'))


class TestCalibrationOverrides(unittest.TestCase):
    """Mirror the calibration rules applied in delta.py and finalize.py."""

    def _apply_delta_calibration(self, findings):
        for f in findings:
            if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
                f['severity'] = 'High'
                f['calibrated'] = True
        return findings

    def _apply_finalize_calibration(self, findings):
        for f in findings:
            if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
                f['severity'] = 'Medium'
        return findings

    def test_unpinned_uses_critical_downgrades_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        result = self._apply_delta_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertTrue(result[0].get('calibrated'))

    def test_unpinned_uses_high_stays_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        result = self._apply_delta_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertNotIn('calibrated', result[0])

    def test_other_rule_critical_not_touched(self):
        findings = [{'short_rule': 'injection', 'severity': 'Critical'}]
        result = self._apply_delta_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Critical')

    def test_secrets_outside_env_high_downgrades_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        result = self._apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')

    def test_secrets_outside_env_medium_not_touched(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        result = self._apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')

    def test_other_rule_high_not_touched_by_finalize(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'High'}]
        result = self._apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')


if __name__ == '__main__':
    unittest.main()
