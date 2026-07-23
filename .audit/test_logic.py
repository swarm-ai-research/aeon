"""
Unit tests for pure logic in classify.py and delta.py.

Run: python .audit/test_logic.py

These tests exercise the two functions that are pure and have no existing
coverage: our_severity() (severity mapping) and fp_for() (fingerprint
generation). They do not touch the filesystem or invoke the audit binaries.
"""
import hashlib
import os
import re
import unittest


# -- Inline copies of the pure functions under test --------------------------
# (Scripts are not importable modules; the functions are pasted here so
#  tests can run without triggering the top-level file I/O in each script.)

def our_severity(f):
    """Copied from .audit/classify.py: maps SARIF level+confidence → severity."""
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
    """Copied from .audit/delta.py: deterministic 16-char hex fingerprint."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# -- our_severity() tests ----------------------------------------------------

class TestOurSeverity(unittest.TestCase):

    def _f(self, level, confidence=None):
        d = {'level': level}
        if confidence is not None:
            d['confidence'] = confidence
        return d

    # Happy-path for all five return branches

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity(self._f('error', 'high')), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'medium')), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'low')), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('warning', 'high')), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'medium')), 'Medium')

    def test_note_is_low(self):
        self.assertEqual(our_severity(self._f('note')), 'Low')

    # Edge cases

    def test_error_missing_confidence_key_is_high_not_critical(self):
        # When the SARIF result has no 'confidence' property at all,
        # .get() returns '' which != 'high', so error → High not Critical.
        self.assertEqual(our_severity(self._f('error')), 'High')

    def test_error_empty_string_confidence_is_high_not_critical(self):
        self.assertEqual(our_severity(self._f('error', '')), 'High')

    def test_confidence_case_insensitive(self):
        # 'HIGH' (upper-case) must still reach Critical via .lower() normalisation.
        self.assertEqual(our_severity(self._f('error', 'HIGH')), 'Critical')

    def test_warning_missing_confidence_key_is_medium(self):
        self.assertEqual(our_severity(self._f('warning')), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', '')), 'Medium')

    def test_unknown_level_is_low(self):
        # Any level not explicitly handled falls through to 'Low'.
        self.assertEqual(our_severity(self._f('none')), 'Low')
        self.assertEqual(our_severity(self._f('')), 'Low')


# -- fp_for() tests ----------------------------------------------------------

class TestFpFor(unittest.TestCase):

    def test_returns_16_char_hex(self):
        fp = fp_for('rule-x', 'file.yml', 'some step')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')

    def test_deterministic(self):
        args = ('unpinned-uses', '.github/workflows/ci.yml', 'Build')
        self.assertEqual(fp_for(*args), fp_for(*args))

    def test_uses_basename_only(self):
        # Full path and bare filename must produce the same fingerprint.
        self.assertEqual(
            fp_for('rule', '.github/workflows/ci.yml', 'step'),
            fp_for('rule', 'ci.yml', 'step'),
        )

    def test_different_rules_differ(self):
        self.assertNotEqual(
            fp_for('rule-a', 'ci.yml', 'step'),
            fp_for('rule-b', 'ci.yml', 'step'),
        )

    def test_different_files_differ(self):
        self.assertNotEqual(
            fp_for('rule', 'ci.yml', 'step'),
            fp_for('rule', 'deploy.yml', 'step'),
        )

    def test_different_steps_differ(self):
        self.assertNotEqual(
            fp_for('rule', 'ci.yml', 'Setup Node'),
            fp_for('rule', 'ci.yml', 'Build'),
        )

    def test_step_underscore_vs_space_differ(self):
        # delta.py explicitly replaces '_' → ' ' before calling fp_for to
        # align prior-audit stored step names with current ones. This test
        # confirms that the raw function treats them as different (the caller
        # is responsible for normalisation).
        self.assertNotEqual(
            fp_for('rule', 'ci.yml', 'Setup_Node'),
            fp_for('rule', 'ci.yml', 'Setup Node'),
        )

    def test_empty_step_allowed(self):
        fp = fp_for('rule', 'ci.yml', '')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')


if __name__ == '__main__':
    unittest.main()
