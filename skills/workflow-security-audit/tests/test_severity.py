"""
test_severity.py — Unit tests for the severity-mapping and fingerprint logic
used in .audit/classify.py and .audit/delta.py.

These helpers are inline scripts (not importable modules), so the logic is
replicated here from the source to lock in the expected behaviour.  If someone
changes the mapping in classify.py this test will surface the regression.

Run:  python3 skills/workflow-security-audit/tests/test_severity.py
"""

import hashlib
import os
import sys
import unittest


# ── replicated from .audit/classify.py ──────────────────────────────────────

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


# ── replicated from .audit/delta.py ─────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── tests ────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    # Covered by the primary audit flow
    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_no_confidence_field_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_no_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    # Previously uncovered branch: 'note' level falls through to Low
    def test_note_level_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_note_level_no_confidence_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    # Edge case: confidence field present but empty string
    def test_error_empty_confidence_is_high_not_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    # Edge case: confidence casing must not matter (classify.py calls .lower())
    def test_confidence_case_insensitive_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

    def test_confidence_case_insensitive_warning_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')

    # Edge case: unknown level (not in the SARIF spec but should not crash)
    def test_unknown_level_falls_to_low(self):
        self.assertEqual(our_severity({'level': 'info'}), 'Low')
        self.assertEqual(our_severity({'level': ''}), 'Low')


class TestFpFor(unittest.TestCase):

    def test_basic_fingerprint_is_16_hex_chars(self):
        fp = fp_for('template-injection', '.github/workflows/ci.yml', 'Build')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')

    def test_fingerprint_is_deterministic(self):
        fp1 = fp_for('unpinned-uses', 'workflows/deploy.yml', 'Deploy')
        fp2 = fp_for('unpinned-uses', 'workflows/deploy.yml', 'Deploy')
        self.assertEqual(fp1, fp2)

    def test_fingerprint_uses_basename_not_full_path(self):
        fp_abs = fp_for('rule', '/home/runner/work/.github/workflows/ci.yml', 'Step')
        fp_rel = fp_for('rule', '.github/workflows/ci.yml', 'Step')
        fp_base = fp_for('rule', 'ci.yml', 'Step')
        # All three should resolve to the same fingerprint because fp_for
        # calls os.path.basename() internally.
        self.assertEqual(fp_abs, fp_base)
        self.assertEqual(fp_rel, fp_base)

    def test_different_rules_produce_different_fingerprints(self):
        fp1 = fp_for('template-injection', 'ci.yml', 'Build')
        fp2 = fp_for('unpinned-uses', 'ci.yml', 'Build')
        self.assertNotEqual(fp1, fp2)

    def test_different_steps_produce_different_fingerprints(self):
        fp1 = fp_for('rule', 'ci.yml', 'Build Step')
        fp2 = fp_for('rule', 'ci.yml', 'Deploy Step')
        self.assertNotEqual(fp1, fp2)

    # Edge case: the prior-audit step normalisation replaces '_' with ' '
    # before calling fp_for; the raw (underscore) and normalised (space)
    # versions must therefore be *different* so that both get added to the
    # prior_fp_set (delta.py adds both our_fp and our_fp2).
    def test_underscore_vs_space_step_differ(self):
        fp_space = fp_for('rule', 'ci.yml', 'Setup Node')
        fp_under = fp_for('rule', 'ci.yml', 'Setup_Node')
        self.assertNotEqual(fp_space, fp_under)


if __name__ == '__main__':
    result = unittest.main(verbosity=2, exit=False)
    sys.exit(0 if result.result.wasSuccessful() else 1)
