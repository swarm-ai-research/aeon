"""Unit tests for pure helper functions shared across .audit/ scripts.

Run with: python -m pytest .audit/test_audit_helpers.py
      or:  python -m unittest .audit.test_audit_helpers

Functions under test are inlined here because the parent scripts have
top-level side effects (file I/O) that prevent clean import.
"""

import hashlib
import os
import re
import unittest


# ---------------------------------------------------------------------------
# our_severity — duplicated identically in classify.py and extract_steps.py
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


class TestOurSeverity(unittest.TestCase):

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_empty_confidence_is_high(self):
        # Empty string is falsy but must not match 'high'
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_confidence_key_is_high(self):
        # .get('confidence', '') default → treated as non-high
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_uppercase_confidence_is_critical(self):
        # .lower() normalises uppercase confidence values from zizmor
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_note_level_no_confidence_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        # Fallback path for any level not explicitly handled
        self.assertEqual(our_severity({'level': 'info'}), 'Low')


# ---------------------------------------------------------------------------
# Fingerprint functions — fp_for (delta.py) vs fp (gen_trailer.py)
#
# These differ in how they handle spaces in step names:
#   fp_for keeps spaces as-is
#   fp     replaces spaces with underscores
#
# This intentional difference exists so delta.py can dual-probe both variants
# when matching against prior audit fingerprints.
# ---------------------------------------------------------------------------

def fp_for(rule, fname, step):
    """delta.py version — preserves spaces in step name."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def fp_gen(rule, fname, step):
    """gen_trailer.py version — normalises spaces to underscores in step name."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class TestFingerprintFunctions(unittest.TestCase):

    def test_fp_for_strips_dir_prefix(self):
        full = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Checkout')
        bare = fp_for('unpinned-uses', 'ci.yml', 'Checkout')
        self.assertEqual(full, bare)

    def test_fp_gen_strips_dir_prefix(self):
        full = fp_gen('unpinned-uses', '.github/workflows/ci.yml', 'Checkout')
        bare = fp_gen('unpinned-uses', 'ci.yml', 'Checkout')
        self.assertEqual(full, bare)

    def test_fp_for_returns_16_hex_chars(self):
        h = fp_for('some-rule', 'ci.yml', 'top')
        self.assertEqual(len(h), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in h))

    def test_fp_gen_returns_16_hex_chars(self):
        h = fp_gen('some-rule', 'ci.yml', 'top')
        self.assertEqual(len(h), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in h))

    def test_space_vs_underscore_produces_different_hashes(self):
        # Documents the intentional divergence between the two variants
        h_space = fp_for('unpinned-uses', 'ci.yml', 'Setup Node')
        h_under = fp_gen('unpinned-uses', 'ci.yml', 'Setup Node')
        self.assertNotEqual(h_space, h_under)

    def test_step_without_spaces_produces_same_hash(self):
        # When step has no spaces both functions must agree
        h1 = fp_for('unpinned-uses', 'ci.yml', 'Checkout')
        h2 = fp_gen('unpinned-uses', 'ci.yml', 'Checkout')
        self.assertEqual(h1, h2)

    def test_fp_for_is_deterministic(self):
        a = fp_for('template-injection', 'deploy.yml', 'Run tests')
        b = fp_for('template-injection', 'deploy.yml', 'Run tests')
        self.assertEqual(a, b)

    def test_different_rules_produce_different_hashes(self):
        h1 = fp_for('unpinned-uses', 'ci.yml', 'top')
        h2 = fp_for('secrets-outside-env', 'ci.yml', 'top')
        self.assertNotEqual(h1, h2)

    def test_different_files_produce_different_hashes(self):
        h1 = fp_for('unpinned-uses', 'ci.yml', 'top')
        h2 = fp_for('unpinned-uses', 'deploy.yml', 'top')
        self.assertNotEqual(h1, h2)


# ---------------------------------------------------------------------------
# Step-name regex — extract_steps.py
# ---------------------------------------------------------------------------

STEP_RE = re.compile(r"\s*-\s*name:\s*[\"']?(.+?)[\"']?\s*$")


class TestStepNameRegex(unittest.TestCase):

    def _match(self, line):
        m = STEP_RE.match(line)
        return m.group(1) if m else None

    def test_unquoted_name(self):
        self.assertEqual(self._match('      - name: Checkout'), 'Checkout')

    def test_double_quoted_name(self):
        self.assertEqual(self._match('      - name: "Setup Node.js"'), 'Setup Node.js')

    def test_single_quoted_name(self):
        self.assertEqual(self._match("      - name: 'Run tests'"), 'Run tests')

    def test_minimal_indentation(self):
        self.assertEqual(self._match('- name: Build'), 'Build')

    def test_name_with_spaces(self):
        self.assertEqual(self._match('    - name: Upload release assets'), 'Upload release assets')

    def test_no_match_for_non_name_line(self):
        self.assertIsNone(self._match('      - uses: actions/checkout@v4'))

    def test_no_match_for_plain_yaml_key(self):
        self.assertIsNone(self._match('      run: echo hello'))

    def test_trailing_whitespace_stripped(self):
        self.assertEqual(self._match('    - name: Build   '), 'Build')

    def test_name_with_colon_inside(self):
        # Step names may contain colons (e.g. "Run: make build")
        self.assertEqual(self._match('    - name: Run: make build'), 'Run: make build')


if __name__ == '__main__':
    unittest.main()
