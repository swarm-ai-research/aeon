"""Tests for audit classification logic used in classify.py / extract_steps.py.

Run: python3 .audit/test_classify.py
"""

import hashlib
import unittest


# --- Replicated from classify.py / extract_steps.py (must stay in sync) ---

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


# Fingerprinting scheme from extract_steps.py: short_rule|file|step
def make_fingerprint(short_rule, file_uri, step):
    fp_src = f"{short_rule}|{file_uri}|{step}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# Fingerprinting scheme from delta.py: short_rule|basename(file)|step
def make_fingerprint_delta(short_rule, file_path, step):
    import os
    base = os.path.basename(file_path)
    fp_src = f"{short_rule}|{base}|{step}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# --------------------------------------------------------------------------


class TestOurSeverity(unittest.TestCase):

    # -- Covered branches --

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_non_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_non_high_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    # -- Missing edge cases --

    def test_note_level_is_low(self):
        # 'note' is the third SARIF level; none of the if-branches match → Low
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_note_level_high_confidence_still_low(self):
        # High confidence does NOT uplift 'note' to Medium/High — only error/warning are checked
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        # Any level not in {error, warning} falls through to Low
        self.assertEqual(our_severity({'level': 'none'}), 'Low')
        self.assertEqual(our_severity({'level': ''}), 'Low')

    def test_missing_confidence_key_error_is_high(self):
        # Missing key → .get() returns '' → not 'high' → error stays High, not Critical
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_missing_confidence_key_warning_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_empty_confidence_error_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_confidence_comparison_is_case_insensitive(self):
        # .lower() is applied before comparison — 'High' and 'HIGH' must match
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')


class TestFingerprintStability(unittest.TestCase):
    """Fingerprint stability is critical: a change in scheme re-tags all prior
    UNCHANGED findings as NEW, flooding the report with false regressions."""

    def test_fingerprint_is_deterministic(self):
        fp1 = make_fingerprint('unpinned-uses', 'aeon.yml', 'Setup Node')
        fp2 = make_fingerprint('unpinned-uses', 'aeon.yml', 'Setup Node')
        self.assertEqual(fp1, fp2)

    def test_fingerprint_length_is_16_hex_chars(self):
        fp = make_fingerprint('unpinned-uses', 'aeon.yml', 'Setup Node')
        self.assertEqual(len(fp), 16)
        int(fp, 16)  # raises ValueError if not valid hex

    def test_fingerprint_differs_on_rule_change(self):
        fp1 = make_fingerprint('unpinned-uses', 'aeon.yml', 'Setup Node')
        fp2 = make_fingerprint('artipacked', 'aeon.yml', 'Setup Node')
        self.assertNotEqual(fp1, fp2)

    def test_fingerprint_differs_on_step_change(self):
        fp1 = make_fingerprint('unpinned-uses', 'aeon.yml', 'Setup Node')
        fp2 = make_fingerprint('unpinned-uses', 'aeon.yml', 'Build')
        self.assertNotEqual(fp1, fp2)

    def test_extract_steps_vs_delta_scheme_match_when_uri_is_basename(self):
        # zizmor SARIF URIs are bare filenames (e.g. "aeon.yml"), so both schemes
        # should agree. If they diverge, delta.py will mark every finding as NEW.
        rule, file_uri, step = 'unpinned-uses', 'aeon.yml', 'Checkout'
        fp_gen = make_fingerprint(rule, file_uri, step)
        fp_delta = make_fingerprint_delta(rule, file_uri, step)
        self.assertEqual(fp_gen, fp_delta)

    def test_extract_steps_vs_delta_scheme_diverge_on_full_path(self):
        # If zizmor ever returns full paths (e.g. ".github/workflows/aeon.yml"),
        # extract_steps.py uses the full path while delta.py normalizes to basename.
        # This mismatch would cause every finding to be flagged as NEW.
        rule, step = 'unpinned-uses', 'Checkout'
        full_path = '.github/workflows/aeon.yml'
        fp_gen = make_fingerprint(rule, full_path, step)
        fp_delta = make_fingerprint_delta(rule, full_path, step)
        self.assertNotEqual(fp_gen, fp_delta, (
            "Schemes diverge on full paths — if zizmor returns absolute URIs, "
            "extract_steps.py must normalize with os.path.basename() too."
        ))


if __name__ == '__main__':
    unittest.main()
