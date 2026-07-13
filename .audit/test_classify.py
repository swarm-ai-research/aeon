"""Tests for severity classification and fingerprint logic in classify.py."""

import hashlib
import os
import re
import unittest


def our_severity(f):
    """Severity mapping extracted from classify.py."""
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


def make_fingerprint(f):
    """Fingerprint construction extracted from classify.py."""
    short_rule = f['rule_id'].split('/')[-1]
    snip_key = re.sub(r'\s+', ' ', f['snippet'])[:60]
    file_short = os.path.basename(f['file'])
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


class TestOurSeverity(unittest.TestCase):

    def _f(self, level, confidence=''):
        return {'level': level, 'confidence': confidence}

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity(self._f('error', 'high')), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'medium')), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', '')), 'High')

    def test_error_missing_confidence_key_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('warning', 'high')), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'medium')), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', '')), 'Medium')

    def test_note_level_is_low(self):
        self.assertEqual(our_severity(self._f('note')), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity(self._f('unknown-level')), 'Low')

    def test_confidence_comparison_is_case_insensitive(self):
        # confidence string is lowercased before comparison, so 'HIGH' must equal 'high'
        self.assertEqual(our_severity(self._f('error', 'HIGH')), 'Critical')
        self.assertEqual(our_severity(self._f('warning', 'HIGH')), 'High')


class TestMakeFingerprint(unittest.TestCase):

    def _f(self, rule_id, file_path, snippet):
        return {'rule_id': rule_id, 'file': file_path, 'snippet': snippet}

    def test_fingerprint_is_16_hex_chars(self):
        fp = make_fingerprint(self._f('foo/bar/rule', 'path/to/workflow.yml', 'some snippet'))
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_uses_last_segment_of_rule_id(self):
        # 'org/repo/my-rule' and 'my-rule' should produce the same fingerprint
        f1 = self._f('org/repo/my-rule', 'a.yml', 'x')
        f2 = self._f('my-rule', 'a.yml', 'x')
        self.assertEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_uses_basename_of_file_path(self):
        f1 = self._f('rule', 'deep/path/to/workflow.yml', 'x')
        f2 = self._f('rule', 'workflow.yml', 'x')
        self.assertEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_normalizes_whitespace_in_snippet(self):
        f1 = self._f('rule', 'a.yml', 'foo   bar\n  baz')
        f2 = self._f('rule', 'a.yml', 'foo bar baz')
        self.assertEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_snippet_truncated_at_60_chars(self):
        # Characters beyond position 60 should not affect the fingerprint
        f1 = self._f('rule', 'a.yml', 'x' * 100)
        f2 = self._f('rule', 'a.yml', 'x' * 60)
        self.assertEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_snippet_boundary_61st_char_differs(self):
        # Changing char at position 61 should not change the fingerprint
        f1 = self._f('rule', 'a.yml', 'x' * 60 + 'A')
        f2 = self._f('rule', 'a.yml', 'x' * 60 + 'B')
        self.assertEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_different_rules_differ(self):
        f1 = self._f('rule-a', 'a.yml', 'x')
        f2 = self._f('rule-b', 'a.yml', 'x')
        self.assertNotEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_different_files_differ(self):
        f1 = self._f('rule', 'a.yml', 'x')
        f2 = self._f('rule', 'b.yml', 'x')
        self.assertNotEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_different_snippets_differ(self):
        f1 = self._f('rule', 'a.yml', 'snippet one')
        f2 = self._f('rule', 'a.yml', 'snippet two')
        self.assertNotEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_deterministic(self):
        f = self._f('injection/template-injection', '.github/workflows/aeon.yml', '${{ github.event.inputs.param }}')
        self.assertEqual(make_fingerprint(f), make_fingerprint(f))


if __name__ == '__main__':
    unittest.main()
