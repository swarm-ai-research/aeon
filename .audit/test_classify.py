"""Unit tests for our_severity() as defined in classify.py and extract_steps.py.

Both scripts contain an identical implementation; this file tests it in isolation
so the logic can be verified without touching the SARIF/JSON files those scripts
require at runtime.

Run: python3 .audit/test_classify.py
"""

import unittest


def our_severity(f):
    """Copied verbatim from classify.py / extract_steps.py."""
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


class TestOurSeverity(unittest.TestCase):

    # --- error-level branches ---

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_conf_mixed_case_is_critical(self):
        # SARIF tools may emit 'High' or 'HIGH'; .lower() must normalise them.
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_absent_conf_is_high(self):
        # confidence key absent → defaults to '' → .lower() == '' → not 'high'
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    # --- warning-level branches ---

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_absent_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    # --- fallthrough / Low branch ---

    def test_note_level_is_low(self):
        # 'note' is a common SARIF level; must not be confused with error/warning.
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({'level': '', 'confidence': 'high'}), 'Low')


if __name__ == '__main__':
    unittest.main()
