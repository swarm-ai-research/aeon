#!/usr/bin/env python3
"""Tests for our_severity() in .audit/classify.py.

Extracts the function directly from source via AST so module-level I/O
(reading parsed.json, writing classified.json) is never triggered.

Run from any directory:
    python3 .audit/test_classify.py
"""
import ast
import os
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))


def _load_our_severity():
    """Compile our_severity() from classify.py without running I/O side-effects."""
    src_path = os.path.join(_HERE, 'classify.py')
    with open(src_path) as f:
        source = f.read()
    tree = ast.parse(source)
    func_node = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == 'our_severity'
    )
    mini = ast.Module(body=[func_node], type_ignores=[])
    ast.fix_missing_locations(mini)
    ns = {}
    exec(compile(mini, src_path, 'exec'), ns)  # noqa: S102
    return ns['our_severity']


our_severity = _load_our_severity()


def _f(level, confidence=''):
    return {'level': level, 'confidence': confidence}


class TestOurSeverity(unittest.TestCase):
    # --- Critical branch ---

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity(_f('error', 'high')), 'Critical')

    # --- High branch (two paths) ---

    def test_error_medium_confidence_is_high_not_critical(self):
        # error without high confidence must not be promoted to Critical
        self.assertEqual(our_severity(_f('error', 'medium')), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity(_f('error', 'low')), 'High')

    def test_error_missing_confidence_is_high(self):
        # confidence key absent → get() defaults to '' → non-high → High
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity(_f('warning', 'high')), 'High')

    # --- Medium branch ---

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity(_f('warning', 'medium')), 'Medium')

    def test_warning_no_confidence_is_medium(self):
        self.assertEqual(our_severity(_f('warning')), 'Medium')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity(_f('warning', 'low')), 'Medium')

    # --- Low branch (catch-all) ---

    def test_note_level_is_low(self):
        # zizmor 'note'-level findings are informational; catch-all maps to Low
        self.assertEqual(our_severity(_f('note')), 'Low')

    def test_note_with_high_confidence_is_still_low(self):
        # note level has no High upgrade path — confidence is irrelevant
        self.assertEqual(our_severity(_f('note', 'high')), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity(_f('unknown')), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity(_f('')), 'Low')

    # --- confidence normalisation ---

    def test_confidence_titlecase_normalised(self):
        # .lower() in the function means 'High' and 'HIGH' both match 'high'
        self.assertEqual(our_severity(_f('error', 'High')), 'Critical')
        self.assertEqual(our_severity(_f('error', 'HIGH')), 'Critical')
        self.assertEqual(our_severity(_f('warning', 'High')), 'High')


if __name__ == '__main__':
    unittest.main()
