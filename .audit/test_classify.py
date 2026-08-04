"""
Unit tests for the severity-classification logic in classify.py.

our_severity() is a pure function; we copy it here so tests run without
triggering classify.py's top-level file I/O (json.load / json.dump).

Run: python .audit/test_classify.py
"""
import unittest


# Copied verbatim from .audit/classify.py — update when the source changes.
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


class TestOurSeverity(unittest.TestCase):

    # --- error level ---

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_conf_key_is_high(self):
        # confidence key absent — .get() defaults to '' so the 'high' branch is skipped
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_high_conf_uppercase_is_critical(self):
        # SARIF emitters sometimes capitalise the value; .lower() must normalise it
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_high_conf_mixedcase_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

    # --- warning level ---

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_empty_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_warning_missing_conf_key_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_warning_high_conf_uppercase_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')

    # --- note / other levels fall through to Low ---

    def test_note_high_conf_is_low(self):
        # 'note' is the default SARIF level — even with high confidence it maps to Low
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_note_empty_conf_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': ''}), 'Low')

    def test_note_missing_conf_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_none_level_is_low(self):
        # 'none' is another valid SARIF level (suppressed / informational)
        self.assertEqual(our_severity({'level': 'none', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'informational'}), 'Low')


if __name__ == '__main__':
    unittest.main()
