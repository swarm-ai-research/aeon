"""
Tests for pure-logic functions extracted from the .audit/ pipeline scripts.
Run with: python -m pytest .audit/test_audit.py  or  python .audit/test_audit.py

Functions under test come from:
  classify.py   -> our_severity()
  delta.py      -> fp_for()
  gen_trailer.py -> fp() (note: normalises spaces to underscores — differs from delta.py)
  summarize_al.py -> categorize_al_finding() (inline logic)
  parse_sarif.py  -> severity resolution priority chain
"""

import hashlib
import os
import unittest


# ── classify.py ──────────────────────────────────────────────────────────────

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


# ── delta.py ─────────────────────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── gen_trailer.py ────────────────────────────────────────────────────────────
# Differs from fp_for: normalises spaces → underscores in step before hashing.

def fp_trailer(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── summarize_al.py ───────────────────────────────────────────────────────────

KNOWN_CODES = ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']


def categorize_al_finding(msg):
    for code in KNOWN_CODES:
        if code in msg:
            return code
    return 'other'


# ── parse_sarif.py severity resolution ───────────────────────────────────────

def resolve_sarif_severity(props):
    """Mirror the `or`-chain on line 16 of parse_sarif.py."""
    return (
        props.get('problem.severity')
        or props.get('zizmor/severity')
        or props.get('security-severity', '')
    )


# ─────────────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    def test_error_high_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_case_insensitive(self):
        # confidence is lowercased before comparison
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_medium_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_missing_confidence_is_high(self):
        # no 'confidence' key → defaults to '' → not 'high' → High branch
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_falls_through_to_low(self):
        # 'note' is the SARIF level zizmor uses for informational findings
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'none'}), 'Low')


class TestFpFor(unittest.TestCase):

    def test_returns_16_hex_chars(self):
        fp = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Checkout')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_only_basename_is_used(self):
        fp1 = fp_for('rule', '.github/workflows/ci.yml', 'step')
        fp2 = fp_for('rule', 'other/path/ci.yml', 'step')
        self.assertEqual(fp1, fp2)

    def test_different_rules_differ(self):
        self.assertNotEqual(fp_for('rule-a', 'f.yml', 's'), fp_for('rule-b', 'f.yml', 's'))

    def test_different_steps_differ(self):
        self.assertNotEqual(fp_for('rule', 'f.yml', 'step-a'), fp_for('rule', 'f.yml', 'step-b'))

    def test_empty_components_produce_valid_fp(self):
        fp = fp_for('', '', '')
        self.assertEqual(len(fp), 16)

    def test_step_spaces_not_normalised(self):
        # delta.py fp_for does NOT replace spaces; gen_trailer.py fp() does.
        # These must differ so that delta.py's dual-lookup (with/without replacement)
        # is necessary and correct.
        fp_space = fp_for('rule', 'f.yml', 'Setup Node')
        fp_under = fp_for('rule', 'f.yml', 'Setup_Node')
        self.assertNotEqual(fp_space, fp_under)


class TestFpTrailer(unittest.TestCase):
    """gen_trailer.py normalises spaces → underscores before hashing."""

    def test_returns_16_hex_chars(self):
        fp = fp_trailer('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        self.assertEqual(len(fp), 16)

    def test_spaces_and_underscores_produce_same_fp(self):
        # gen_trailer stores with underscores, so "Setup Node" == "Setup_Node"
        self.assertEqual(
            fp_trailer('rule', 'f.yml', 'Setup Node'),
            fp_trailer('rule', 'f.yml', 'Setup_Node'),
        )

    def test_trailer_differs_from_delta_fp_for_spaced_steps(self):
        # This asymmetry is why delta.py must try both variants when matching
        # prior fingerprints emitted by gen_trailer.py.
        self.assertNotEqual(
            fp_trailer('rule', 'f.yml', 'Setup Node'),
            fp_for('rule', 'f.yml', 'Setup Node'),
        )


class TestCategorizeAlFinding(unittest.TestCase):

    def test_sc2086_detected(self):
        self.assertEqual(categorize_al_finding('SC2086: Double quote to prevent globbing'), 'SC2086')

    def test_sc2046_detected(self):
        self.assertEqual(categorize_al_finding('SC2046: Quote this to prevent word splitting'), 'SC2046')

    def test_sc2034_detected(self):
        self.assertEqual(categorize_al_finding('SC2034: appears unused'), 'SC2034')

    def test_first_code_in_list_wins_when_multiple_codes_present(self):
        # KNOWN_CODES order: SC2086 before SC2046; if both appear, SC2086 wins
        self.assertEqual(categorize_al_finding('SC2086 and SC2046 both here'), 'SC2086')

    def test_unknown_code_returns_other(self):
        self.assertEqual(categorize_al_finding('some unrecognised linting message'), 'other')

    def test_empty_message_returns_other(self):
        self.assertEqual(categorize_al_finding(''), 'other')

    def test_partial_code_match_does_not_trigger(self):
        # 'SC208' is not in KNOWN_CODES and does not substring-match any entry
        self.assertEqual(categorize_al_finding('error: SC208'), 'other')


class TestResolveSarifSeverity(unittest.TestCase):

    def test_problem_severity_preferred(self):
        props = {'problem.severity': 'high', 'zizmor/severity': 'medium', 'security-severity': 'low'}
        self.assertEqual(resolve_sarif_severity(props), 'high')

    def test_zizmor_severity_is_fallback(self):
        props = {'zizmor/severity': 'medium', 'security-severity': 'low'}
        self.assertEqual(resolve_sarif_severity(props), 'medium')

    def test_security_severity_is_last_resort(self):
        self.assertEqual(resolve_sarif_severity({'security-severity': 'low'}), 'low')

    def test_empty_props_returns_empty_string(self):
        self.assertEqual(resolve_sarif_severity({}), '')

    def test_falsy_problem_severity_falls_through(self):
        # Empty string is falsy; the `or` chain advances to the next key.
        props = {'problem.severity': '', 'zizmor/severity': 'medium'}
        self.assertEqual(resolve_sarif_severity(props), 'medium')

    def test_none_problem_severity_falls_through(self):
        props = {'problem.severity': None, 'zizmor/severity': 'high'}
        self.assertEqual(resolve_sarif_severity(props), 'high')


if __name__ == '__main__':
    unittest.main()
