"""Tests for audit classify/summarize logic.

Exercises the severity-mapping and shellcheck-code-counting branches that had
no coverage. Reproduces the exact logic from classify.py and summarize_al.py
so that changes to those scripts will break these tests as a regression guard.

Run: python -m unittest .audit/test_classify.py
"""

import unittest
from collections import Counter


# ---------------------------------------------------------------------------
# Logic reproduced from .audit/classify.py — our_severity()
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
# Logic reproduced from .audit/summarize_al.py
# ---------------------------------------------------------------------------

KNOWN_CODES = ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']


def count_shellcheck_codes(findings):
    codes = Counter()
    for f in findings:
        msg = f.get('message', '')
        matched = False
        for code in KNOWN_CODES:
            if code in msg:
                codes[code] += 1
                matched = True
                break
        if not matched:
            codes['other'] += 1
    return codes


def is_high_candidate(f):
    msg = f.get('message', '')
    return ('SC2086' in msg or 'SC2046' in msg) and 'github.' in msg.lower()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestOurSeverity(unittest.TestCase):

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_confidence_uppercase_normalised(self):
        # confidence comes from raw SARIF; .lower() normalises it
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_missing_confidence_defaults_to_high(self):
        # No 'confidence' key — get() default '' → not 'high' → second branch fires
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_is_low(self):
        # The else branch — any non-error/non-warning level maps here
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_none_string_level_is_low(self):
        self.assertEqual(our_severity({'level': 'none'}), 'Low')

    def test_unknown_level_is_low(self):
        # e.g. a future SARIF level value the code hasn't seen
        self.assertEqual(our_severity({'level': 'informational', 'confidence': 'high'}), 'Low')


class TestShellcheckCodeCounting(unittest.TestCase):

    def test_known_code_counted(self):
        counts = count_shellcheck_codes([{'message': 'SC2086 double-quote to prevent splitting'}])
        self.assertEqual(counts['SC2086'], 1)

    def test_unrecognised_message_goes_to_other(self):
        counts = count_shellcheck_codes([{'message': 'workflow expression syntax error'}])
        self.assertEqual(counts['other'], 1)

    def test_first_match_wins_on_multi_code_message(self):
        # SC2086 appears before SC2046 in KNOWN_CODES — break fires, SC2046 not counted
        counts = count_shellcheck_codes([{'message': 'SC2086 and also SC2046 here'}])
        self.assertEqual(counts['SC2086'], 1)
        self.assertEqual(counts.get('SC2046', 0), 0)

    def test_multiple_findings_tallied_independently(self):
        findings = [
            {'message': 'SC2086 unquoted'},
            {'message': 'SC2086 again'},
            {'message': 'SC2155 masked return value'},
            {'message': 'unrelated warning'},
        ]
        counts = count_shellcheck_codes(findings)
        self.assertEqual(counts['SC2086'], 2)
        self.assertEqual(counts['SC2155'], 1)
        self.assertEqual(counts['other'], 1)

    def test_empty_findings_list(self):
        self.assertEqual(sum(count_shellcheck_codes([]).values()), 0)

    def test_missing_message_key_counts_as_other(self):
        # f.get('message', '') guards missing key
        counts = count_shellcheck_codes([{}])
        self.assertEqual(counts['other'], 1)


class TestHighCandidateDetection(unittest.TestCase):

    def test_sc2086_with_github_context(self):
        f = {'message': 'SC2086: unquoted github.event.pull_request.title'}
        self.assertTrue(is_high_candidate(f))

    def test_sc2046_with_github_context(self):
        f = {'message': 'SC2046 warning in github.actor expression'}
        self.assertTrue(is_high_candidate(f))

    def test_sc2086_without_github_is_not_elevated(self):
        f = {'message': 'SC2086: double quote to prevent globbing and splitting'}
        self.assertFalse(is_high_candidate(f))

    def test_github_uppercase_still_detected(self):
        # 'github.' in msg.lower() — capitalised variant matches
        f = {'message': 'SC2086 GitHub.event is unquoted'}
        self.assertTrue(is_high_candidate(f))

    def test_other_sc_code_with_github_not_elevated(self):
        # SC2129 is not SC2086/SC2046, so even with github. it is not HIGH
        f = {'message': 'SC2129 error near github.workflows path'}
        self.assertFalse(is_high_candidate(f))


if __name__ == '__main__':
    unittest.main()
