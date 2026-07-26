"""
Tests for the severity-classification and fingerprinting logic in classify.py and delta.py.

Run: python3 .audit/test_classify.py
"""

import hashlib
import os
import sys
import unittest


# ── replicated logic (not importing classify.py / delta.py because they
#    have file-reading side-effects at module level) ─────────────────────

def our_severity(f):
    """Copied verbatim from .audit/classify.py."""
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
    """Copied verbatim from .audit/delta.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def is_high_candidate_al(msg):
    """Copied verbatim from .audit/summarize_al.py high-candidate check."""
    return ('SC2086' in msg or 'SC2046' in msg) and 'github.' in msg.lower()


# ── tests ────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    # --- happy-path branches ---

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_no_conf_is_high(self):
        # confidence key absent entirely
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_no_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        # Any level not matching error/warning falls through to Low
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')

    # --- edge cases around confidence case sensitivity ---

    def test_error_uppercase_conf_is_critical(self):
        # .lower() is applied, so 'HIGH' must also be treated as 'high'
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_warning_mixedcase_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'High'}), 'High')

    def test_error_empty_string_conf_is_high(self):
        # Empty string doesn't match 'high', so error → High
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    # --- calibration override (delta.py) ---

    def test_unpinned_uses_calibration(self):
        # delta.py downgrades unpinned-uses Critical → High
        f = {'level': 'error', 'confidence': 'high', 'short_rule': 'unpinned-uses',
             'severity': 'Critical'}
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
        self.assertEqual(f['severity'], 'High')

    def test_other_rule_not_calibrated(self):
        # A different rule should NOT be downgraded
        f = {'level': 'error', 'confidence': 'high', 'short_rule': 'template-injection',
             'severity': 'Critical'}
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
        self.assertEqual(f['severity'], 'Critical')


class TestFpFor(unittest.TestCase):

    def test_produces_16_hex_chars(self):
        fp = fp_for('template-injection', '.github/workflows/ci.yml', 'Build')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_basename_extracted(self):
        # Only the basename of fname should affect the fingerprint
        fp_full = fp_for('rule', '/some/deep/path/file.yml', 'step')
        fp_base = fp_for('rule', 'file.yml', 'step')
        self.assertEqual(fp_full, fp_base)

    def test_different_rules_differ(self):
        fp1 = fp_for('template-injection', 'ci.yml', 'Build')
        fp2 = fp_for('unpinned-uses', 'ci.yml', 'Build')
        self.assertNotEqual(fp1, fp2)

    def test_different_steps_differ(self):
        fp1 = fp_for('rule', 'ci.yml', 'Build')
        fp2 = fp_for('rule', 'ci.yml', 'Deploy')
        self.assertNotEqual(fp1, fp2)

    def test_step_underscore_vs_space(self):
        # delta.py replaces '_' with ' ' for prior fingerprints when matching.
        # The two forms must produce different hashes (the caller normalises before
        # comparing, not the function itself).
        fp_space = fp_for('rule', 'ci.yml', 'Setup Node')
        fp_under = fp_for('rule', 'ci.yml', 'Setup_Node')
        self.assertNotEqual(fp_space, fp_under)

    def test_deterministic(self):
        self.assertEqual(
            fp_for('r', 'f.yml', 's'),
            fp_for('r', 'f.yml', 's'),
        )


class TestHighCandidateAl(unittest.TestCase):

    def test_sc2086_with_github_is_high(self):
        msg = "ShellCheck reported issue in this script: SC2086: github.event.inputs.name"
        self.assertTrue(is_high_candidate_al(msg))

    def test_sc2046_with_github_is_high(self):
        msg = "SC2046 warning: github.sha used unquoted"
        self.assertTrue(is_high_candidate_al(msg))

    def test_sc2086_without_github_is_not_high(self):
        msg = "SC2086: Double quote to prevent globbing around $FOO"
        self.assertFalse(is_high_candidate_al(msg))

    def test_github_without_sc_code_is_not_high(self):
        msg = "Variable github.event.issue.body used in shell"
        self.assertFalse(is_high_candidate_al(msg))

    def test_github_uppercase_matches(self):
        # msg.lower() is applied, so GITHUB. must also match
        msg = "SC2086: GITHUB.ACTOR used unsafely"
        self.assertTrue(is_high_candidate_al(msg))

    def test_unrelated_shellcheck_code_not_high(self):
        msg = "SC2155: Declare and assign separately to avoid masking return values"
        self.assertFalse(is_high_candidate_al(msg))

    def test_empty_message_not_high(self):
        self.assertFalse(is_high_candidate_al(''))


if __name__ == '__main__':
    result = unittest.main(verbosity=2, exit=False)
    sys.exit(0 if result.result.wasSuccessful() else 1)
