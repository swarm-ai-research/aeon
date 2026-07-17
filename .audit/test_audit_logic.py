"""
Unit tests for pure functions extracted from the .audit/ pipeline scripts.

Run: python -m pytest .audit/test_audit_logic.py -v
  or: python .audit/test_audit_logic.py

Covers uncovered branches in:
  classify.py / extract_steps.py  — our_severity()
  classify.py                      — snippet-based fingerprint
  extract_steps.py / delta.py      — step-based fingerprint (fp_for)
  gen_trailer.py                   — space→underscore normalization in fp()
  extract_steps.py                 — step-name regex (quoted / unquoted)
  delta.py                         — aggregate file matching (substring edge case)
  delta2.py                        — short_rule() split
"""

import hashlib
import os
import re
import unittest

# ---------------------------------------------------------------------------
# Functions duplicated from the scripts (they are scripts, not modules).
# Each copy is kept byte-for-byte identical to the production version.
# ---------------------------------------------------------------------------

def our_severity(f):
    """From classify.py and extract_steps.py."""
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


def classify_fingerprint(short_rule, file_path, snippet):
    """From classify.py — snippet-keyed fingerprint."""
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(file_path)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


def step_fingerprint(short_rule, file_path, step):
    """From extract_steps.py — step-name-keyed fingerprint."""
    fp_src = f"{short_rule}|{file_path}|{step}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


def fp_for(rule, fname, step):
    """From delta.py — step-name-keyed, uses basename(fname)."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def gen_trailer_fp(rule, fname, step):
    """From gen_trailer.py — step spaces replaced with underscores."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


STEP_RE = re.compile(r"\s*-\s*name:\s*[\"']?(.+?)[\"']?\s*$")


def extract_step_name(line):
    """From extract_steps.py — parse a YAML step name line."""
    m = STEP_RE.match(line)
    return m.group(1).strip() if m else None


def short_rule(s):
    """From delta2.py — last component of a rule_id after '/'."""
    return s.split('/')[-1]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestOurSeverity(unittest.TestCase):

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_confidence_is_high(self):
        # confidence key absent — .get() returns '' which is not 'high'
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_note_level_is_low(self):
        # 'note' is zizmor's lowest level — falls through to the else branch
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'medium'}), 'Low')
        self.assertEqual(our_severity({'level': 'note', 'confidence': ''}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')
        self.assertEqual(our_severity({'level': '', 'confidence': 'high'}), 'Low')

    def test_confidence_case_folded(self):
        # The scripts call .lower() — uppercase 'High' must map identically to 'high'
        self.assertEqual(
            our_severity({'level': 'error', 'confidence': 'High'}),
            our_severity({'level': 'error', 'confidence': 'high'}),
        )
        self.assertEqual(
            our_severity({'level': 'warning', 'confidence': 'HIGH'}),
            our_severity({'level': 'warning', 'confidence': 'high'}),
        )


class TestClassifyFingerprint(unittest.TestCase):

    def test_returns_16_hex_chars(self):
        fp = classify_fingerprint('unpinned-uses', 'aeon.yml', 'uses: actions/checkout@v4')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')

    def test_deterministic(self):
        args = ('template-injection', '.github/workflows/aeon.yml', 'echo "${{ github.event.inputs.foo }}"')
        self.assertEqual(classify_fingerprint(*args), classify_fingerprint(*args))

    def test_uses_basename_not_full_path(self):
        # classify.py uses os.path.basename — different dirs, same basename → same fp
        fp1 = classify_fingerprint('rule', '.github/workflows/aeon.yml', 'snip')
        fp2 = classify_fingerprint('rule', 'aeon.yml', 'snip')
        self.assertEqual(fp1, fp2)

    def test_different_rules_produce_different_fps(self):
        fp1 = classify_fingerprint('rule-a', 'aeon.yml', 'snip')
        fp2 = classify_fingerprint('rule-b', 'aeon.yml', 'snip')
        self.assertNotEqual(fp1, fp2)

    def test_snippet_normalises_whitespace(self):
        # Multi-space / tab in snippet gets collapsed to a single space
        fp1 = classify_fingerprint('rule', 'f.yml', 'a  b\tc')
        fp2 = classify_fingerprint('rule', 'f.yml', 'a b c')
        self.assertEqual(fp1, fp2)

    def test_snippet_truncated_at_60_chars(self):
        long_snip = 'x' * 100
        same_snip = 'x' * 60
        self.assertEqual(
            classify_fingerprint('rule', 'f.yml', long_snip),
            classify_fingerprint('rule', 'f.yml', same_snip),
        )


class TestStepFingerprint(unittest.TestCase):
    """extract_steps.py uses the full file path (not basename) in its fingerprint."""

    def test_returns_16_hex_chars(self):
        fp = step_fingerprint('unpinned-uses', 'aeon.yml', 'Checkout')
        self.assertEqual(len(fp), 16)

    def test_full_path_matters(self):
        fp1 = step_fingerprint('rule', '.github/workflows/aeon.yml', 'step')
        fp2 = step_fingerprint('rule', 'aeon.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_different_steps_produce_different_fps(self):
        fp1 = step_fingerprint('rule', 'f.yml', 'Setup Node')
        fp2 = step_fingerprint('rule', 'f.yml', 'Run tests')
        self.assertNotEqual(fp1, fp2)


class TestFpFor(unittest.TestCase):
    """delta.py's fp_for() — uses basename, no underscore replacement."""

    def test_returns_16_hex_chars(self):
        fp = fp_for('unpinned-uses', '.github/workflows/aeon.yml', 'Checkout')
        self.assertEqual(len(fp), 16)

    def test_uses_basename(self):
        fp1 = fp_for('rule', '.github/workflows/aeon.yml', 'step')
        fp2 = fp_for('rule', 'aeon.yml', 'step')
        self.assertEqual(fp1, fp2)

    def test_space_and_underscore_produce_different_fps(self):
        # delta.py does NOT normalise spaces — 'Setup Node' ≠ 'Setup_Node'
        fp1 = fp_for('rule', 'f.yml', 'Setup Node')
        fp2 = fp_for('rule', 'f.yml', 'Setup_Node')
        self.assertNotEqual(fp1, fp2)


class TestGenTrailerFp(unittest.TestCase):
    """gen_trailer.py's fp() — replaces spaces with underscores before hashing."""

    def test_returns_16_hex_chars(self):
        fp = gen_trailer_fp('rule', 'aeon.yml', 'Setup Node')
        self.assertEqual(len(fp), 16)

    def test_space_replaced_by_underscore(self):
        # gen_trailer uses 'Setup_Node' in the trailer line, then delta.py must
        # re-derive the same fp — confirm the normalisation round-trips.
        fp_space = gen_trailer_fp('rule', 'f.yml', 'Setup Node')
        fp_under = gen_trailer_fp('rule', 'f.yml', 'Setup_Node')
        self.assertEqual(fp_space, fp_under)

    def test_no_spaces_unaffected(self):
        fp1 = gen_trailer_fp('rule', 'f.yml', 'Checkout')
        fp2 = fp_for('rule', 'f.yml', 'Checkout')
        self.assertEqual(fp1, fp2)


class TestExtractStepName(unittest.TestCase):

    def test_unquoted_name(self):
        self.assertEqual(extract_step_name('      - name: Setup Node'), 'Setup Node')

    def test_single_quoted_name(self):
        self.assertEqual(extract_step_name("      - name: 'Setup Node'"), 'Setup Node')

    def test_double_quoted_name(self):
        self.assertEqual(extract_step_name('      - name: "Run tests"'), 'Run tests')

    def test_no_leading_spaces(self):
        self.assertEqual(extract_step_name('- name: Checkout'), 'Checkout')

    def test_non_name_line_returns_none(self):
        self.assertIsNone(extract_step_name('      - uses: actions/checkout@v4'))
        self.assertIsNone(extract_step_name('      run: echo hello'))
        self.assertIsNone(extract_step_name(''))

    def test_name_with_colon(self):
        # Step names can include colons
        result = extract_step_name('      - name: Build: production')
        self.assertIsNotNone(result)
        self.assertIn('Build', result)

    def test_trailing_whitespace_stripped(self):
        result = extract_step_name('      - name: Setup Node   ')
        self.assertEqual(result, 'Setup Node')


class TestShortRule(unittest.TestCase):

    def test_splits_on_slash(self):
        self.assertEqual(short_rule('zizmor/unpinned-uses'), 'unpinned-uses')
        self.assertEqual(short_rule('github/codeql-action/secrets-outside-env'), 'secrets-outside-env')

    def test_no_slash_returns_whole(self):
        self.assertEqual(short_rule('template-injection'), 'template-injection')

    def test_empty_string(self):
        self.assertEqual(short_rule(''), '')


class TestAggregateFileMatching(unittest.TestCase):
    """
    Covers the substring-match branch in delta.py:
        if base in files or any(base in fl for fl in files)

    The second condition (substring) can produce false positives when a short
    basename is contained inside a longer filename string.
    """

    @staticmethod
    def _matches(base_name, files_str):
        files = files_str.split(',')
        return base_name in files or any(base_name in fl for fl in files)

    def test_exact_match(self):
        self.assertTrue(self._matches('aeon.yml', 'aeon.yml,fleet-runner.yml'))

    def test_no_match(self):
        self.assertFalse(self._matches('lint.yml', 'aeon.yml,fleet-runner.yml'))

    def test_substring_false_positive(self):
        # 'aeon.yml' is a substring of 'sync-aeon.yml' — the any() branch fires
        # even though 'aeon.yml' is not literally in the comma list.
        # This test documents the existing behaviour (not a bug fix).
        files_str = 'sync-aeon.yml'
        result = self._matches('aeon.yml', files_str)
        # The substring match fires: 'aeon.yml' IS in 'sync-aeon.yml'
        self.assertTrue(result, "substring match fires for 'aeon.yml' inside 'sync-aeon.yml'")

    def test_exact_match_preferred_over_substring(self):
        # When the exact name IS in the list, it matches regardless of substring
        self.assertTrue(self._matches('aeon.yml', 'aeon.yml'))

    def test_empty_files_string(self):
        self.assertFalse(self._matches('aeon.yml', ''))


if __name__ == '__main__':
    unittest.main(verbosity=2)
