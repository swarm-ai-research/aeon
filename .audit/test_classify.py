"""
Tests for the severity classification and fingerprinting logic used by the
workflow-security-audit skill. These functions live in classify.py and delta.py
but are reproduced inline here because those scripts load JSON from disk on import.

Run: python3 .audit/test_classify.py
"""

import hashlib
import os
import unittest


# ── Reproduce logic from classify.py ───────────────────────────────────────

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


# ── Reproduce logic from delta.py ──────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Tests ──────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    def _f(self, level, confidence=None):
        d = {'level': level}
        if confidence is not None:
            d['confidence'] = confidence
        return d

    # Primary branches
    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity(self._f('error', 'high')), 'Critical')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'low')), 'High')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'medium')), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('warning', 'high')), 'High')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'low')), 'Medium')

    def test_note_level_is_low(self):
        self.assertEqual(our_severity(self._f('note')), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity(self._f('none')), 'Low')

    # Edge cases: missing / empty confidence key
    def test_error_missing_confidence_is_high(self):
        # .get('confidence', '') returns '' when key absent → not 'high' → High
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', '')), 'High')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', '')), 'Medium')

    # Edge cases: case-insensitive confidence
    def test_error_uppercase_HIGH_confidence_is_critical(self):
        # .lower() normalises 'HIGH' → 'high'
        self.assertEqual(our_severity(self._f('error', 'HIGH')), 'Critical')

    def test_warning_mixed_case_High_is_high(self):
        self.assertEqual(our_severity(self._f('warning', 'High')), 'High')

    # Confidence that is 'high' for an error must not accidentally produce Medium
    def test_error_high_never_produces_medium(self):
        self.assertNotEqual(our_severity(self._f('error', 'high')), 'Medium')

    # note/Low edge: extra confidence value has no effect
    def test_note_with_high_confidence_still_low(self):
        self.assertEqual(our_severity(self._f('note', 'high')), 'Low')


class TestFpFor(unittest.TestCase):

    def test_returns_16_hex_chars(self):
        fp = fp_for('unpinned-uses', 'workflows/ci.yml', 'Setup Node')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_strips_directory_prefix(self):
        # fp_for strips the directory so only basename participates in the hash
        fp_full = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'step')
        fp_base = fp_for('unpinned-uses', 'ci.yml', 'step')
        self.assertEqual(fp_full, fp_base)

    def test_different_rules_produce_different_fingerprints(self):
        fp1 = fp_for('rule-a', 'ci.yml', 'step')
        fp2 = fp_for('rule-b', 'ci.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_different_steps_produce_different_fingerprints(self):
        fp1 = fp_for('rule', 'ci.yml', 'Setup Node')
        fp2 = fp_for('rule', 'ci.yml', 'Setup_Node')
        self.assertNotEqual(fp1, fp2)

    def test_different_files_produce_different_fingerprints(self):
        fp1 = fp_for('rule', 'ci.yml', 'step')
        fp2 = fp_for('rule', 'deploy.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_empty_step_produces_valid_fingerprint(self):
        fp = fp_for('rule', 'ci.yml', '')
        self.assertEqual(len(fp), 16)

    def test_deterministic(self):
        fp1 = fp_for('unpinned-uses', 'ci.yml', 'Build')
        fp2 = fp_for('unpinned-uses', 'ci.yml', 'Build')
        self.assertEqual(fp1, fp2)

    def test_path_with_trailing_slash_uses_empty_basename(self):
        # os.path.basename('dir/') returns '' — documents the known behaviour
        fp_dir = fp_for('rule', 'workflows/', 'step')
        fp_empty = fp_for('rule', '', 'step')
        self.assertEqual(fp_dir, fp_empty)


if __name__ == '__main__':
    unittest.main()
