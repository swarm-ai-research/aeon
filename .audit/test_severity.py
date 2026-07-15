"""Unit tests for pure functions extracted from .audit/ pipeline scripts.

Run with: python -m pytest .audit/test_severity.py  (or python .audit/test_severity.py)
No file-system fixtures required — only pure logic is tested.
"""

import hashlib
import os
import re
import unittest


# --- Extracted from classify.py / extract_steps.py (identical logic) ---

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


# --- Extracted from delta.py ---

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# --- Extracted from gen_trailer.py ---

def fp_gen(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# --- Extracted from delta.py / delta2.py ---

def short_rule(rule_id):
    return rule_id.split('/')[-1]


class TestOurSeverity(unittest.TestCase):
    """Tests for the 5-branch severity mapping used by classify and extract_steps."""

    def _f(self, level, confidence=''):
        return {'level': level, 'confidence': confidence}

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity(self._f('error', 'high')), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'medium')), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'low')), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', '')), 'High')

    def test_error_missing_confidence_key_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('warning', 'high')), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'medium')), 'Medium')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'low')), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', '')), 'Medium')

    def test_note_level_is_low(self):
        self.assertEqual(our_severity(self._f('note')), 'Low')

    def test_none_level_is_low(self):
        self.assertEqual(our_severity(self._f('none')), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity(self._f('info')), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity(self._f('')), 'Low')

    def test_confidence_case_insensitive(self):
        # confidence is lowercased before comparison
        self.assertEqual(our_severity(self._f('error', 'HIGH')), 'Critical')
        self.assertEqual(our_severity(self._f('warning', 'HIGH')), 'High')

    def test_error_level_not_affected_by_note_confidence(self):
        # 'note' as confidence doesn't change error -> High path
        self.assertEqual(our_severity(self._f('error', 'note')), 'High')


class TestFingerprintFunctions(unittest.TestCase):
    """Tests for sha256-based fingerprint helpers in delta.py and gen_trailer.py."""

    def test_fp_for_returns_16_hex_chars(self):
        result = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Checkout')
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_fp_gen_returns_16_hex_chars(self):
        result = fp_gen('unpinned-uses', '.github/workflows/ci.yml', 'Checkout repo')
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_fp_for_uses_basename_not_full_path(self):
        r1 = fp_for('rule', '.github/workflows/ci.yml', 'step')
        r2 = fp_for('rule', 'ci.yml', 'step')
        self.assertEqual(r1, r2)

    def test_fp_gen_uses_basename_not_full_path(self):
        r1 = fp_gen('rule', '.github/workflows/ci.yml', 'step')
        r2 = fp_gen('rule', 'ci.yml', 'step')
        self.assertEqual(r1, r2)

    def test_fp_for_different_rules_differ(self):
        r1 = fp_for('rule-a', 'ci.yml', 'step')
        r2 = fp_for('rule-b', 'ci.yml', 'step')
        self.assertNotEqual(r1, r2)

    def test_fp_for_different_steps_differ(self):
        r1 = fp_for('rule', 'ci.yml', 'Setup Node')
        r2 = fp_for('rule', 'ci.yml', 'Build')
        self.assertNotEqual(r1, r2)

    def test_fp_gen_replaces_spaces_with_underscores(self):
        # fp_gen('rule', 'ci.yml', 'Setup Node') == fp_for with 'Setup_Node'
        r_gen = fp_gen('rule', 'ci.yml', 'Setup Node')
        r_manual = hashlib.sha256(b'rule|ci.yml|Setup_Node').hexdigest()[:16]
        self.assertEqual(r_gen, r_manual)

    def test_fp_for_does_not_replace_spaces(self):
        r_for = fp_for('rule', 'ci.yml', 'Setup Node')
        r_manual = hashlib.sha256(b'rule|ci.yml|Setup Node').hexdigest()[:16]
        self.assertEqual(r_for, r_manual)

    def test_fp_for_and_fp_gen_diverge_when_step_has_spaces(self):
        # This documents the known divergence between the two functions.
        r1 = fp_for('rule', 'ci.yml', 'Setup Node')
        r2 = fp_gen('rule', 'ci.yml', 'Setup Node')
        self.assertNotEqual(r1, r2)

    def test_fp_for_and_fp_gen_agree_when_step_has_no_spaces(self):
        r1 = fp_for('rule', 'ci.yml', 'checkout')
        r2 = fp_gen('rule', 'ci.yml', 'checkout')
        self.assertEqual(r1, r2)

    def test_fp_for_deterministic(self):
        r1 = fp_for('secrets-outside-env', 'deploy.yml', 'top')
        r2 = fp_for('secrets-outside-env', 'deploy.yml', 'top')
        self.assertEqual(r1, r2)


class TestShortRule(unittest.TestCase):
    """Tests for the rule-id basename extractor used in delta2.py."""

    def test_namespaced_rule(self):
        self.assertEqual(short_rule('zizmor/unpinned-uses'), 'unpinned-uses')

    def test_already_short(self):
        self.assertEqual(short_rule('unpinned-uses'), 'unpinned-uses')

    def test_multi_segment(self):
        self.assertEqual(short_rule('a/b/c'), 'c')

    def test_empty_string(self):
        self.assertEqual(short_rule(''), '')


class TestAggregateFilesEdgeCases(unittest.TestCase):
    """Edge cases in aggregate-entry files-list parsing from delta.py / delta2.py."""

    def _parse_files(self, files_str):
        files = files_str.split(',')
        if not files or files == ['']:
            return []
        return [f for f in files if f]

    def test_empty_files_string_returns_empty(self):
        self.assertEqual(self._parse_files(''), [])

    def test_single_file(self):
        self.assertEqual(self._parse_files('ci.yml'), ['ci.yml'])

    def test_multiple_files(self):
        self.assertEqual(self._parse_files('ci.yml,deploy.yml'), ['ci.yml', 'deploy.yml'])

    def test_trailing_comma_produces_no_empty_entry(self):
        result = self._parse_files('ci.yml,')
        self.assertNotIn('', result)


if __name__ == '__main__':
    unittest.main()
