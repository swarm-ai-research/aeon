"""
Tests for pure functions in classify.py, extract_steps.py, and delta.py.

These scripts are not importable (they execute at module level), so the
pure functions are replicated here verbatim for testing.

Run: python .audit/test_classify.py
"""

import hashlib
import os
import unittest


# --- Replicated from classify.py / extract_steps.py ---

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


def fingerprint_from_step(short_rule, file_uri, step):
    """Fingerprint scheme used in extract_steps.py / delta.py."""
    fp_src = f"{short_rule}|{file_uri}|{step}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# --- Replicated from delta.py ---

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_uppercase_conf_is_critical(self):
        # Confidence is lowercased before comparison — 'HIGH' must still resolve to Critical.
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_conf_is_high(self):
        # confidence key absent — .get() falls back to ''
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_uppercase_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')

    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_empty_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_warning_missing_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_note_high_conf_is_still_low(self):
        # note-level findings are always Low regardless of confidence
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'unknown'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({'level': ''}), 'Low')


class TestFpFor(unittest.TestCase):

    def test_returns_16_hex_chars(self):
        result = fp_for('unpinned-uses', 'aeon.yml', 'Setup Node')
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_basename_stripped(self):
        # fp_for strips the directory component — result must match bare filename
        with_path = fp_for('unpinned-uses', '.github/workflows/aeon.yml', 'Setup Node')
        bare = fp_for('unpinned-uses', 'aeon.yml', 'Setup Node')
        self.assertEqual(with_path, bare)

    def test_different_steps_differ(self):
        fp1 = fp_for('unpinned-uses', 'aeon.yml', 'Setup Node')
        fp2 = fp_for('unpinned-uses', 'aeon.yml', 'Install Deps')
        self.assertNotEqual(fp1, fp2)

    def test_different_rules_differ(self):
        fp1 = fp_for('unpinned-uses', 'aeon.yml', 'Setup Node')
        fp2 = fp_for('artipacked', 'aeon.yml', 'Setup Node')
        self.assertNotEqual(fp1, fp2)

    def test_different_files_differ(self):
        fp1 = fp_for('unpinned-uses', 'aeon.yml', 'Setup Node')
        fp2 = fp_for('unpinned-uses', 'lint.yml', 'Setup Node')
        self.assertNotEqual(fp1, fp2)

    def test_deterministic(self):
        # Same inputs always produce the same fingerprint
        fp1 = fp_for('template-injection', 'messages.yml', 'top')
        fp2 = fp_for('template-injection', 'messages.yml', 'top')
        self.assertEqual(fp1, fp2)

    def test_underscore_vs_space_differ(self):
        # Prior audit stored steps with underscores; delta.py normalises with .replace('_', ' ')
        # before calling fp_for — so the raw (underscore) and normalised (space) variants
        # must produce different fingerprints (normalisation happens in the caller, not here).
        fp_under = fp_for('unpinned-uses', 'aeon.yml', 'Setup_Node')
        fp_space = fp_for('unpinned-uses', 'aeon.yml', 'Setup Node')
        self.assertNotEqual(fp_under, fp_space)


class TestFingerprintFromStep(unittest.TestCase):
    """Tests for the extract_steps.py fingerprint scheme (uses full file URI, not basename)."""

    def test_returns_16_hex_chars(self):
        result = fingerprint_from_step('unpinned-uses', 'aeon.yml', 'top')
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_full_path_differs_from_basename(self):
        # extract_steps.py uses the raw file URI; delta.py uses basename via fp_for.
        # These two schemes intentionally differ and should NOT match.
        full = fingerprint_from_step('unpinned-uses', '.github/workflows/aeon.yml', 'top')
        base = fp_for('unpinned-uses', '.github/workflows/aeon.yml', 'top')
        self.assertNotEqual(full, base)

    def test_deterministic(self):
        fp1 = fingerprint_from_step('artipacked', 'lint.yml', 'Build')
        fp2 = fingerprint_from_step('artipacked', 'lint.yml', 'Build')
        self.assertEqual(fp1, fp2)


if __name__ == '__main__':
    unittest.main()
