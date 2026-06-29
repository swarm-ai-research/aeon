"""
Unit tests for pure logic extracted from .audit/ scripts.

Functions under test come from:
  classify.py / extract_steps.py  -> our_severity()
  delta.py                         -> fp_for()
  parse_sarif.py                   -> extract_severity()
  delta.py                         -> file_matches_aggregate()
  classify.py / delta2.py          -> short_rule (split logic)

Run with:
  python -m pytest .audit/test_audit_logic.py -v
  # or
  python .audit/test_audit_logic.py
"""
import hashlib
import os
import unittest


# ---------------------------------------------------------------------------
# Functions reproduced verbatim from classify.py / extract_steps.py
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


# ---------------------------------------------------------------------------
# Function reproduced verbatim from delta.py
# ---------------------------------------------------------------------------

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Severity-priority chain from parse_sarif.py
# ---------------------------------------------------------------------------

def extract_severity(props):
    return (
        props.get('problem.severity')
        or props.get('zizmor/severity')
        or props.get('security-severity', '')
    )


# ---------------------------------------------------------------------------
# Aggregate file matching from delta.py
# ---------------------------------------------------------------------------

def file_matches_aggregate(base, files):
    return base in files or any(base in fl for fl in files)


# ===========================================================================
# Tests
# ===========================================================================

class TestOurSeverity(unittest.TestCase):

    # ── Critical branch ──────────────────────────────────────────────────
    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    # ── High branch (error, non-high conf) ───────────────────────────────
    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_missing_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    # ── High branch (warning, high conf) ─────────────────────────────────
    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    # ── Medium branch ────────────────────────────────────────────────────
    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_missing_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    # ── Low branch (catch-all) ────────────────────────────────────────────
    def test_note_level_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'none'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({'level': ''}), 'Low')

    # ── Case sensitivity ──────────────────────────────────────────────────
    def test_conf_case_normalised_for_critical(self):
        # zizmor may emit 'High' with capital H — .lower() must normalise it
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

    def test_conf_case_normalised_for_warning_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')


class TestFpFor(unittest.TestCase):

    def test_deterministic(self):
        fp1 = fp_for('unpinned-uses', 'deploy.yml', 'Checkout')
        fp2 = fp_for('unpinned-uses', 'deploy.yml', 'Checkout')
        self.assertEqual(fp1, fp2)

    def test_returns_16_hex_chars(self):
        fp = fp_for('some-rule', 'workflow.yml', 'Build')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp), fp)

    def test_different_rules_differ(self):
        fp1 = fp_for('rule-a', 'workflow.yml', 'Build')
        fp2 = fp_for('rule-b', 'workflow.yml', 'Build')
        self.assertNotEqual(fp1, fp2)

    def test_different_files_differ(self):
        fp1 = fp_for('rule', 'foo.yml', 'Build')
        fp2 = fp_for('rule', 'bar.yml', 'Build')
        self.assertNotEqual(fp1, fp2)

    def test_full_path_and_basename_match(self):
        # delta.py uses os.path.basename() — full path resolves to same fp as basename
        fp1 = fp_for('rule', '.github/workflows/foo.yml', 'Build')
        fp2 = fp_for('rule', 'foo.yml', 'Build')
        self.assertEqual(fp1, fp2)

    def test_step_space_vs_underscore_differ(self):
        # delta.py comment notes this as the source of the underscore/space delta issue;
        # callers must normalise before comparing across audit runs
        fp_space = fp_for('rule', 'foo.yml', 'Setup Node')
        fp_under = fp_for('rule', 'foo.yml', 'Setup_Node')
        self.assertNotEqual(fp_space, fp_under)

    def test_different_steps_differ(self):
        fp1 = fp_for('rule', 'foo.yml', 'step-a')
        fp2 = fp_for('rule', 'foo.yml', 'step-b')
        self.assertNotEqual(fp1, fp2)

    def test_empty_strings_produce_valid_fp(self):
        fp = fp_for('', '', '')
        self.assertEqual(len(fp), 16)


class TestExtractSeverity(unittest.TestCase):

    def test_problem_severity_wins_over_zizmor(self):
        props = {'problem.severity': 'high', 'zizmor/severity': 'medium', 'security-severity': '5.0'}
        self.assertEqual(extract_severity(props), 'high')

    def test_zizmor_severity_fallback(self):
        props = {'zizmor/severity': 'medium', 'security-severity': '7.5'}
        self.assertEqual(extract_severity(props), 'medium')

    def test_security_severity_last_resort(self):
        props = {'security-severity': '7.5'}
        self.assertEqual(extract_severity(props), '7.5')

    def test_empty_props_returns_empty_string(self):
        self.assertEqual(extract_severity({}), '')

    def test_empty_string_problem_severity_falls_through(self):
        # '' is falsy → should fall through to zizmor/severity
        props = {'problem.severity': '', 'zizmor/severity': 'low'}
        self.assertEqual(extract_severity(props), 'low')

    def test_none_problem_severity_falls_through(self):
        # None is falsy → should fall through to zizmor/severity
        props = {'problem.severity': None, 'zizmor/severity': 'low'}
        self.assertEqual(extract_severity(props), 'low')

    def test_all_falsy_returns_empty_string(self):
        props = {'problem.severity': None, 'zizmor/severity': '', 'security-severity': ''}
        self.assertEqual(extract_severity(props), '')


class TestFileMatchesAggregate(unittest.TestCase):

    def test_exact_match_in_list(self):
        self.assertTrue(file_matches_aggregate('foo.yml', ['foo.yml', 'bar.yml']))

    def test_no_match(self):
        self.assertFalse(file_matches_aggregate('baz.yml', ['foo.yml', 'bar.yml']))

    def test_substring_match(self):
        # 'foo.yml' is a substring of 'prefix_foo.yml' — this is intentional/documented
        # behaviour but can produce false positives for short basenames
        self.assertTrue(file_matches_aggregate('foo.yml', ['prefix_foo.yml']))

    def test_empty_files_list_returns_false(self):
        self.assertFalse(file_matches_aggregate('foo.yml', []))

    def test_single_blank_entry_no_match(self):
        self.assertFalse(file_matches_aggregate('foo.yml', ['']))


class TestShortRule(unittest.TestCase):

    def test_slash_separated_id_takes_last_segment(self):
        self.assertEqual('zizmor/unpinned-uses'.split('/')[-1], 'unpinned-uses')

    def test_no_slash_returns_whole_string(self):
        self.assertEqual('simple-rule'.split('/')[-1], 'simple-rule')

    def test_multiple_slashes_takes_last(self):
        self.assertEqual('org/category/rule-name'.split('/')[-1], 'rule-name')

    def test_empty_string(self):
        self.assertEqual(''.split('/')[-1], '')

    def test_trailing_slash(self):
        self.assertEqual('zizmor/'.split('/')[-1], '')


if __name__ == '__main__':
    unittest.main()
