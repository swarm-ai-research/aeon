#!/usr/bin/env python3
"""
Tests for the severity-classification logic in classify.py.

classify.py is a procedural script, not a module, so we load it with
importlib while mocking the file-I/O that executes at module level.
Run: python3 .audit/test_classify.py
"""
import hashlib
import importlib.util
import os
import re
import unittest
from unittest.mock import MagicMock, patch

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLASSIFY_PATH = os.path.join(_HERE, 'classify.py')


def _load_classify():
    """Import classify.py with its file-I/O patched out."""
    with patch('builtins.open', MagicMock()), \
         patch('json.load', return_value=[]), \
         patch('json.dump'), \
         patch('builtins.print'):
        spec = importlib.util.spec_from_file_location('classify_mod', _CLASSIFY_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    return mod


class TestOurSeverity(unittest.TestCase):
    """
    Unit tests for our_severity() in classify.py.

    Severity mapping:
      error + high confidence  → Critical
      error (other confidence) → High
      warning + high           → High
      warning (other)          → Medium
      anything else            → Low
    """

    @classmethod
    def setUpClass(cls):
        mod = _load_classify()
        cls.sev = staticmethod(mod.our_severity)

    # ── Critical ──────────────────────────────────────────────────────────────
    def test_error_high_is_critical(self):
        self.assertEqual(self.sev({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_confidence_case_insensitive(self):
        # classify.py applies .lower(), so 'High' must map to Critical too
        self.assertEqual(self.sev({'level': 'error', 'confidence': 'High'}), 'Critical')

    # ── High (error branch) ───────────────────────────────────────────────────
    def test_error_medium_confidence_is_high(self):
        self.assertEqual(self.sev({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(self.sev({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(self.sev({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_confidence_key_is_high(self):
        # .get('confidence', '') returns '' when key is absent
        self.assertEqual(self.sev({'level': 'error'}), 'High')

    # ── High (warning branch) ─────────────────────────────────────────────────
    def test_warning_high_confidence_is_high(self):
        self.assertEqual(self.sev({'level': 'warning', 'confidence': 'high'}), 'High')

    # ── Medium ────────────────────────────────────────────────────────────────
    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(self.sev({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(self.sev({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(self.sev({'level': 'warning'}), 'Medium')

    # ── Low (else branch) ─────────────────────────────────────────────────────
    def test_note_level_is_low(self):
        # SARIF 'note' level is the third standard level; always Low here
        self.assertEqual(self.sev({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(self.sev({'level': 'none'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(self.sev({'level': ''}), 'Low')


class TestFingerprintContract(unittest.TestCase):
    """
    The fingerprint algorithm in classify.py's module loop is:
      short_rule = rule_id.split('/')[-1]
      snip_key   = re.sub(r'\s+', ' ', snippet)[:60]
      file_short = os.path.basename(file)
      fp_src     = f"{short_rule}|{file_short}|{snip_key}"
      fingerprint = sha256(fp_src).hexdigest()[:16]

    These tests pin the expected behaviour so regressions are caught.
    """

    def _fp(self, rule_id, filepath, snippet):
        short_rule = rule_id.split('/')[-1]
        snip_key = re.sub(r'\s+', ' ', snippet)[:60]
        file_short = os.path.basename(filepath)
        fp_src = f"{short_rule}|{file_short}|{snip_key}"
        return hashlib.sha256(fp_src.encode()).hexdigest()[:16]

    def test_slash_in_rule_id_uses_last_segment(self):
        fp1 = self._fp('zizmor/unpinned-uses', 'a.yml', '')
        fp2 = self._fp('unpinned-uses', 'a.yml', '')
        self.assertEqual(fp1, fp2)

    def test_no_slash_rule_id_uses_full_id(self):
        fp = self._fp('unpinned-uses', 'a.yml', 'x')
        self.assertEqual(len(fp), 16)

    def test_whitespace_normalised_in_snippet(self):
        fp1 = self._fp('r', 'f.yml', 'a  b\tc\nd')
        fp2 = self._fp('r', 'f.yml', 'a b c d')
        self.assertEqual(fp1, fp2)

    def test_snippet_truncated_at_60_chars(self):
        fp1 = self._fp('r', 'f.yml', 'x' * 100)
        fp2 = self._fp('r', 'f.yml', 'x' * 60)
        self.assertEqual(fp1, fp2)

    def test_full_path_collapses_to_basename(self):
        fp1 = self._fp('r', '.github/workflows/aeon.yml', '')
        fp2 = self._fp('r', 'aeon.yml', '')
        self.assertEqual(fp1, fp2)

    def test_empty_snippet_gives_stable_fingerprint(self):
        fp = self._fp('r', 'f.yml', '')
        self.assertEqual(len(fp), 16)

    def test_fingerprint_is_deterministic(self):
        self.assertEqual(self._fp('r', 'f.yml', 'x'), self._fp('r', 'f.yml', 'x'))

    def test_different_rules_give_different_fingerprints(self):
        self.assertNotEqual(self._fp('rule-a', 'f.yml', ''), self._fp('rule-b', 'f.yml', ''))


if __name__ == '__main__':
    unittest.main(verbosity=2)
