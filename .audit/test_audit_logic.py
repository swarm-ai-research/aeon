"""
Unit tests for pure-function logic in the .audit/ scripts.
Tests are self-contained — they replicate the function bodies verbatim
so that production scripts (which open files at module level) don't need
to be importable as modules.
"""
import hashlib
import os
import unittest
from collections import Counter


# ---------------------------------------------------------------------------
# Logic replicated from classify.py
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Logic replicated from delta.py
# ---------------------------------------------------------------------------

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Logic replicated from parse_sarif.py  (severity field resolution)
# ---------------------------------------------------------------------------

def resolve_severity(props):
    return (
        props.get('problem.severity')
        or props.get('zizmor/severity')
        or props.get('security-severity', '')
    )


# ---------------------------------------------------------------------------
# Logic replicated from summarize_al.py
# ---------------------------------------------------------------------------

SHELLCHECK_CODES = ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']


def categorize_message(msg):
    for code in SHELLCHECK_CODES:
        if code in msg:
            return code
    return 'other'


def is_high_candidate(finding):
    msg = finding.get('message', '')
    return (
        ('SC2086' in msg or 'SC2046' in msg)
        and 'github.' in msg.lower()
    )


# ===========================================================================
# Tests
# ===========================================================================

class TestOurSeverity(unittest.TestCase):

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_confidence_case_insensitive(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_no_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_no_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_any_confidence_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'medium'}), 'Low')
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_other_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info'}), 'Low')
        self.assertEqual(our_severity({'level': ''}), 'Low')


class TestFpFor(unittest.TestCase):

    def test_deterministic(self):
        fp1 = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        fp2 = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        self.assertEqual(fp1, fp2)

    def test_length_is_16_hex_chars(self):
        fp = fp_for('some-rule', 'path/to/file.yml', 'my step')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_uses_basename_not_full_path(self):
        fp_full = fp_for('rule', '/a/b/c/workflow.yml', 'step')
        fp_base = fp_for('rule', 'workflow.yml', 'step')
        self.assertEqual(fp_full, fp_base)

    def test_different_rules_differ(self):
        fp1 = fp_for('rule-a', 'file.yml', 'step')
        fp2 = fp_for('rule-b', 'file.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_different_files_differ(self):
        fp1 = fp_for('rule', 'a.yml', 'step')
        fp2 = fp_for('rule', 'b.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_different_steps_differ(self):
        fp1 = fp_for('rule', 'file.yml', 'step-a')
        fp2 = fp_for('rule', 'file.yml', 'step-b')
        self.assertNotEqual(fp1, fp2)

    def test_underscore_vs_space_step_differs(self):
        # delta.py normalises prior stored "Setup_Node" → "Setup Node" before hashing;
        # this test documents that the raw strings produce different fingerprints,
        # which is why delta.py tries both variants.
        fp_space = fp_for('rule', 'file.yml', 'Setup Node')
        fp_under = fp_for('rule', 'file.yml', 'Setup_Node')
        self.assertNotEqual(fp_space, fp_under)


class TestResolveSeverity(unittest.TestCase):

    def test_problem_severity_takes_priority(self):
        props = {
            'problem.severity': 'critical',
            'zizmor/severity': 'high',
            'security-severity': '9.0',
        }
        self.assertEqual(resolve_severity(props), 'critical')

    def test_zizmor_severity_is_fallback(self):
        props = {
            'zizmor/severity': 'medium',
            'security-severity': '5.0',
        }
        self.assertEqual(resolve_severity(props), 'medium')

    def test_security_severity_is_last_resort(self):
        props = {'security-severity': '7.5'}
        self.assertEqual(resolve_severity(props), '7.5')

    def test_empty_props_returns_empty_string(self):
        self.assertEqual(resolve_severity({}), '')

    def test_falsy_first_field_falls_through(self):
        # An empty string in problem.severity should fall through to the next field.
        props = {'problem.severity': '', 'zizmor/severity': 'low'}
        self.assertEqual(resolve_severity(props), 'low')


class TestCategorizeMessage(unittest.TestCase):

    def test_sc2086_detected(self):
        self.assertEqual(categorize_message('shellcheck: SC2086: Double quote to prevent globbing'), 'SC2086')

    def test_sc2046_detected(self):
        self.assertEqual(categorize_message('SC2046 quote this to prevent word splitting'), 'SC2046')

    def test_first_code_wins(self):
        # Message contains both SC2086 and SC2046; SC2086 appears first in SHELLCHECK_CODES
        msg = 'SC2086 and SC2046 found'
        self.assertEqual(categorize_message(msg), 'SC2086')

    def test_sc2129_detected(self):
        self.assertEqual(categorize_message('SC2129: use >> instead'), 'SC2129')

    def test_unknown_code_is_other(self):
        self.assertEqual(categorize_message('some unrelated lint message'), 'other')

    def test_empty_message_is_other(self):
        self.assertEqual(categorize_message(''), 'other')


class TestIsHighCandidate(unittest.TestCase):

    def test_sc2086_with_github_ref_is_candidate(self):
        f = {'message': 'SC2086: double-quote $github.event.pull_request.title'}
        self.assertTrue(is_high_candidate(f))

    def test_sc2046_with_github_ref_is_candidate(self):
        f = {'message': 'SC2046 quote ${{ github.actor }} to prevent splitting'}
        self.assertTrue(is_high_candidate(f))

    def test_sc2086_without_github_not_candidate(self):
        f = {'message': 'SC2086: double-quote $MY_VAR'}
        self.assertFalse(is_high_candidate(f))

    def test_github_ref_without_sc_code_not_candidate(self):
        f = {'message': 'github.event.inputs.value used here'}
        self.assertFalse(is_high_candidate(f))

    def test_github_case_insensitive(self):
        f = {'message': 'SC2086 value from GITHUB.EVENT.inputs.x'}
        self.assertTrue(is_high_candidate(f))

    def test_missing_message_key(self):
        self.assertFalse(is_high_candidate({}))


if __name__ == '__main__':
    unittest.main()
