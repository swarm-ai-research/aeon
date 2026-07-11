"""
Tests for pure helper functions used by the .audit/ pipeline scripts.

Run with: python3 -m pytest .audit/test_audit_utils.py -v
or:        python3 .audit/test_audit_utils.py
"""

import hashlib
import os
import unittest


# ── our_severity ────────────────────────────────────────────────────────────
# Logic extracted from classify.py / extract_steps.py (identical in both).

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
# Logic extracted from delta.py.

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── fp (gen_trailer) ─────────────────────────────────────────────────────────
# Logic extracted from gen_trailer.py.

def fp_trailer(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class TestOurSeverity(unittest.TestCase):

    # Happy-path: all four branches
    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_no_confidence_key_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_no_confidence_key_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'unknown'}), 'Low')

    # Edge cases: confidence comparisons are case-insensitive via .lower()
    def test_error_uppercase_HIGH_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_warning_mixedcase_High_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'High'}), 'High')

    # Low confidence should not uplift warning
    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')


class TestFpFor(unittest.TestCase):

    def test_returns_16_hex_chars(self):
        result = fp_for('unpinned-uses', 'aeon.yml', 'Checkout')
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_full_path_same_as_basename(self):
        # fp_for uses os.path.basename internally — full path and bare name must match
        fp_full = fp_for('unpinned-uses', '.github/workflows/aeon.yml', 'Checkout')
        fp_base = fp_for('unpinned-uses', 'aeon.yml', 'Checkout')
        self.assertEqual(fp_full, fp_base)

    def test_different_rules_differ(self):
        fp1 = fp_for('unpinned-uses', 'aeon.yml', 'Checkout')
        fp2 = fp_for('secrets-outside-env', 'aeon.yml', 'Checkout')
        self.assertNotEqual(fp1, fp2)

    def test_different_steps_differ(self):
        fp1 = fp_for('unpinned-uses', 'aeon.yml', 'Checkout')
        fp2 = fp_for('unpinned-uses', 'aeon.yml', 'Build')
        self.assertNotEqual(fp1, fp2)

    def test_empty_step_is_stable(self):
        result = fp_for('unpinned-uses', 'aeon.yml', '')
        self.assertEqual(len(result), 16)

    def test_deterministic(self):
        self.assertEqual(
            fp_for('unpinned-uses', 'aeon.yml', 'Checkout'),
            fp_for('unpinned-uses', 'aeon.yml', 'Checkout'),
        )


class TestFpTrailer(unittest.TestCase):

    def test_spaces_in_step_replaced_by_underscore(self):
        # "Setup Node" and "Setup_Node" must yield the same fingerprint
        fp_space = fp_trailer('unpinned-uses', 'aeon.yml', 'Setup Node')
        fp_under = fp_trailer('unpinned-uses', 'aeon.yml', 'Setup_Node')
        self.assertEqual(fp_space, fp_under)

    def test_full_path_same_as_basename(self):
        fp_full = fp_trailer('unpinned-uses', '.github/workflows/aeon.yml', 'Checkout')
        fp_base = fp_trailer('unpinned-uses', 'aeon.yml', 'Checkout')
        self.assertEqual(fp_full, fp_base)

    def test_differs_from_fp_for_due_to_space_normalization(self):
        # fp_for does NOT replace spaces; fp_trailer does.
        # A step with a space must produce different results in the two functions.
        fp_f = fp_for('unpinned-uses', 'aeon.yml', 'Setup Node')
        fp_t = fp_trailer('unpinned-uses', 'aeon.yml', 'Setup Node')
        # fp_trailer replaces ' ' with '_' before hashing, fp_for does not
        self.assertNotEqual(fp_f, fp_t)

    def test_returns_16_hex_chars(self):
        result = fp_trailer('unpinned-uses', 'aeon.yml', 'Checkout')
        self.assertEqual(len(result), 16)


if __name__ == '__main__':
    unittest.main()
