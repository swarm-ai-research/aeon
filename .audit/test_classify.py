"""
Tests for pure logic in the .audit pipeline scripts.

classify.py and gen_trailer.py/delta.py cannot be imported directly because
they perform file I/O at module level.  The pure functions are reproduced here
so their branch coverage and fingerprint-contract can be verified without
touching external files.
"""

import hashlib
import os
import unittest


# ── Logic from classify.py ───────────────────────────────────────────────────

def our_severity(f):
    """Map a parsed SARIF finding dict to Critical / High / Medium / Low."""
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


# ── Logic from gen_trailer.py ────────────────────────────────────────────────

def fp_trailer(rule, fname, step):
    """Fingerprint used when *emitting* new findings into the trailer."""
    s = f"{rule}|{os.path.basename(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Logic from delta.py ──────────────────────────────────────────────────────

def fp_delta(rule, fname, step):
    """Fingerprint used when *reading* prior findings from the trailer."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ─────────────────────────────────────────────────────────────────────────────


class TestOurSeverity(unittest.TestCase):

    # Branch 1: error + high → Critical
    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    # Branch 1 edge: case-insensitive (classify.py lower-cases confidence)
    def test_error_HIGH_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    # Branch 2: error + non-high → High
    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    # Branch 2 edge: missing confidence key defaults to '' via .get()
    def test_error_missing_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    # Branch 3: warning + high → High
    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    # Branch 4: warning + non-high → Medium
    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    # Branch 5: anything else → Low
    def test_note_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_note_no_confidence_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')


class TestFingerprints(unittest.TestCase):

    # ── fp_trailer (gen_trailer.py) ──────────────────────────────────────────

    def test_trailer_fp_is_16_hex_chars(self):
        h = fp_trailer('unpinned-uses', '.github/workflows/aeon.yml', 'Checkout')
        self.assertEqual(len(h), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in h))

    def test_trailer_fp_is_deterministic(self):
        h1 = fp_trailer('template-injection', 'foo.yml', 'Run tests')
        h2 = fp_trailer('template-injection', 'foo.yml', 'Run tests')
        self.assertEqual(h1, h2)

    def test_trailer_fp_uses_basename(self):
        h_abs = fp_trailer('rule', '/full/path/to/file.yml', 'step')
        h_base = fp_trailer('rule', 'file.yml', 'step')
        self.assertEqual(h_abs, h_base)

    def test_trailer_fp_space_normalised_to_underscore(self):
        # gen_trailer.py replaces spaces with underscores before hashing so
        # "Run tests" and "Run_tests" produce the same fingerprint.
        h_spaces = fp_trailer('rule', 'file.yml', 'Run tests')
        h_underscores = fp_trailer('rule', 'file.yml', 'Run_tests')
        self.assertEqual(h_spaces, h_underscores)

    def test_trailer_fp_differs_by_rule(self):
        h1 = fp_trailer('rule-a', 'file.yml', 'step')
        h2 = fp_trailer('rule-b', 'file.yml', 'step')
        self.assertNotEqual(h1, h2)

    def test_trailer_fp_differs_by_file(self):
        h1 = fp_trailer('rule', 'a.yml', 'step')
        h2 = fp_trailer('rule', 'b.yml', 'step')
        self.assertNotEqual(h1, h2)

    def test_trailer_fp_differs_by_step(self):
        h1 = fp_trailer('rule', 'file.yml', 'step-a')
        h2 = fp_trailer('rule', 'file.yml', 'step-b')
        self.assertNotEqual(h1, h2)

    # ── fp_delta (delta.py) ──────────────────────────────────────────────────

    def test_delta_fp_uses_basename(self):
        h1 = fp_delta('rule', '/path/to/file.yml', 'step')
        h2 = fp_delta('rule', 'file.yml', 'step')
        self.assertEqual(h1, h2)

    def test_delta_fp_is_deterministic(self):
        h1 = fp_delta('rule', 'file.yml', 'step')
        h2 = fp_delta('rule', 'file.yml', 'step')
        self.assertEqual(h1, h2)

    def test_delta_fp_length_is_16(self):
        h = fp_delta('unpinned-uses', 'aeon.yml', 'Checkout repo')
        self.assertEqual(len(h), 16)

    # ── Cross-function contract ───────────────────────────────────────────────

    def test_trailer_and_delta_differ_when_step_has_spaces(self):
        # fp_trailer normalises "My Step" → "My_Step" before hashing.
        # fp_delta does NOT — it stores/matches the raw string.
        # This intentional asymmetry means delta.py must try BOTH the
        # underscore and space variants when matching prior fingerprints.
        h_trailer = fp_trailer('rule', 'f.yml', 'My Step')
        h_delta_spaces = fp_delta('rule', 'f.yml', 'My Step')
        h_delta_underscore = fp_delta('rule', 'f.yml', 'My_Step')
        # trailer matches delta with underscores (both hash "rule|f.yml|My_Step")
        self.assertEqual(h_trailer, h_delta_underscore)
        # but NOT delta with raw spaces (hashes "rule|f.yml|My Step")
        self.assertNotEqual(h_trailer, h_delta_spaces)

    def test_trailer_and_delta_agree_when_step_has_no_spaces(self):
        h1 = fp_trailer('rule', 'f.yml', 'Checkout')
        h2 = fp_delta('rule', 'f.yml', 'Checkout')
        self.assertEqual(h1, h2)


if __name__ == '__main__':
    unittest.main()
