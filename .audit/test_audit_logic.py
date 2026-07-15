"""
Unit tests for pure logic extracted from the .audit/ pipeline scripts.
Run with: python -m pytest .audit/test_audit_logic.py -v
         or: python .audit/test_audit_logic.py
No file I/O; all functions are inlined from their source scripts.
"""

import hashlib
import os
import unittest


# ---------------------------------------------------------------------------
# Logic from classify.py and extract_steps.py
# ---------------------------------------------------------------------------

def our_severity(f):
    """Map (level, confidence) to a severity string."""
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
# Logic from delta.py
# ---------------------------------------------------------------------------

def fp_for(rule, fname, step):
    """Fingerprint used in delta.py (space-preserving, basename only)."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Logic from gen_trailer.py
# ---------------------------------------------------------------------------

def fp_trailer(rule, fname, step):
    """Fingerprint used in gen_trailer.py (spaces → underscores)."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Calibration helpers (from delta.py / delta2.py / finalize.py)
# ---------------------------------------------------------------------------

def apply_calibration(findings):
    """Apply all calibration overrides to a list of finding dicts (mutates in-place)."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append('downgraded')


# ---------------------------------------------------------------------------
# Short-rule extraction (from classify.py / extract_steps.py)
# ---------------------------------------------------------------------------

def short_rule(rule_id):
    return rule_id.split('/')[-1]


# ---------------------------------------------------------------------------
# Delta tagging (from delta3.py): for each (rule, file) pair, first
# `prior_count` findings (sorted by line) are UNCHANGED, the rest are NEW.
# ---------------------------------------------------------------------------

def tag_findings(findings, prior_counts):
    """
    Tag each finding with 'NEW' or 'UNCHANGED'.
    prior_counts: dict mapping (short_rule, basename) -> int
    Mutates findings in-place and returns them.
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for f in findings:
        key = (f['short_rule'], os.path.basename(f['file']))
        groups[key].append(f)

    for key, group in groups.items():
        group_sorted = sorted(group, key=lambda x: x['line'])
        p = prior_counts.get(key, 0)
        for i, f in enumerate(group_sorted):
            f['delta'] = 'UNCHANGED' if i < p else 'NEW'
    return findings


# ===========================================================================
# Tests
# ===========================================================================

class TestOurSeverity(unittest.TestCase):

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_confidence_case_insensitive(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_note_with_high_confidence_still_low(self):
        # note level is NOT uplifted regardless of confidence
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info'}), 'Low')
        self.assertEqual(our_severity({'level': ''}), 'Low')


class TestFingerprintFunctions(unittest.TestCase):

    def test_fp_for_basic(self):
        fp = fp_for('unpinned-uses', 'aeon.yml', 'Checkout')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_fp_for_strips_directory(self):
        fp_bare = fp_for('unpinned-uses', 'aeon.yml', 'Checkout')
        fp_path = fp_for('unpinned-uses', '.github/workflows/aeon.yml', 'Checkout')
        self.assertEqual(fp_bare, fp_path)

    def test_fp_for_different_rules_differ(self):
        fp1 = fp_for('unpinned-uses', 'aeon.yml', 'Checkout')
        fp2 = fp_for('artipacked', 'aeon.yml', 'Checkout')
        self.assertNotEqual(fp1, fp2)

    def test_fp_for_different_files_differ(self):
        fp1 = fp_for('unpinned-uses', 'aeon.yml', 'Checkout')
        fp2 = fp_for('unpinned-uses', 'lint.yml', 'Checkout')
        self.assertNotEqual(fp1, fp2)

    def test_fp_trailer_spaces_become_underscores(self):
        # gen_trailer.py replaces spaces with underscores in step name
        fp_spaces = fp_trailer('unpinned-uses', 'aeon.yml', 'Setup Node')
        fp_underscores = fp_trailer('unpinned-uses', 'aeon.yml', 'Setup_Node')
        self.assertEqual(fp_spaces, fp_underscores)

    def test_fp_for_vs_fp_trailer_differ_on_spaced_step(self):
        # delta.py (fp_for) and gen_trailer.py (fp_trailer) use different
        # space handling; results differ for multi-word step names
        fp_delta = fp_for('unpinned-uses', 'aeon.yml', 'Setup Node')
        fp_trailer_ = fp_trailer('unpinned-uses', 'aeon.yml', 'Setup Node')
        self.assertNotEqual(fp_delta, fp_trailer_)

    def test_fp_for_deterministic(self):
        fp1 = fp_for('secrets-outside-env', 'fleet-runner.yml', 'top')
        fp2 = fp_for('secrets-outside-env', 'fleet-runner.yml', 'top')
        self.assertEqual(fp1, fp2)


class TestShortRule(unittest.TestCase):

    def test_slash_suffix_extracted(self):
        self.assertEqual(short_rule('zizmor/unpinned-uses'), 'unpinned-uses')

    def test_no_slash_returns_whole_string(self):
        self.assertEqual(short_rule('unpinned-uses'), 'unpinned-uses')

    def test_multiple_slashes_takes_last(self):
        self.assertEqual(short_rule('a/b/unpinned-uses'), 'unpinned-uses')

    def test_empty_string(self):
        self.assertEqual(short_rule(''), '')


class TestCalibration(unittest.TestCase):

    def _finding(self, rule, severity):
        return {'short_rule': rule, 'severity': severity}

    def test_unpinned_uses_critical_downgraded_to_high(self):
        findings = [self._finding('unpinned-uses', 'Critical')]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertTrue(findings[0].get('calibrated'))

    def test_unpinned_uses_high_unchanged(self):
        findings = [self._finding('unpinned-uses', 'High')]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertFalse(findings[0].get('calibrated', False))

    def test_unpinned_uses_medium_unchanged(self):
        findings = [self._finding('unpinned-uses', 'Medium')]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        findings = [self._finding('secrets-outside-env', 'High')]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_secrets_outside_env_medium_unchanged(self):
        findings = [self._finding('secrets-outside-env', 'Medium')]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_other_rule_critical_unchanged(self):
        findings = [self._finding('artipacked', 'Critical')]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')

    def test_multiple_findings_calibrated_independently(self):
        findings = [
            self._finding('unpinned-uses', 'Critical'),
            self._finding('secrets-outside-env', 'High'),
            self._finding('artipacked', 'High'),
        ]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertEqual(findings[1]['severity'], 'Medium')
        self.assertEqual(findings[2]['severity'], 'High')


class TestTagFindings(unittest.TestCase):

    def _finding(self, rule, fname, line):
        return {
            'short_rule': rule,
            'file': fname,
            'line': line,
            'severity': 'High',
        }

    def test_all_new_when_no_prior(self):
        findings = [
            self._finding('unpinned-uses', 'aeon.yml', 10),
            self._finding('unpinned-uses', 'aeon.yml', 20),
        ]
        tag_findings(findings, {})
        self.assertTrue(all(f['delta'] == 'NEW' for f in findings))

    def test_all_unchanged_when_prior_equals_count(self):
        findings = [
            self._finding('unpinned-uses', 'aeon.yml', 10),
            self._finding('unpinned-uses', 'aeon.yml', 20),
        ]
        tag_findings(findings, {('unpinned-uses', 'aeon.yml'): 2})
        self.assertTrue(all(f['delta'] == 'UNCHANGED' for f in findings))

    def test_first_findings_unchanged_rest_new(self):
        findings = [
            self._finding('unpinned-uses', 'aeon.yml', 10),
            self._finding('unpinned-uses', 'aeon.yml', 20),
            self._finding('unpinned-uses', 'aeon.yml', 30),
        ]
        tag_findings(findings, {('unpinned-uses', 'aeon.yml'): 2})
        sorted_f = sorted(findings, key=lambda x: x['line'])
        self.assertEqual(sorted_f[0]['delta'], 'UNCHANGED')
        self.assertEqual(sorted_f[1]['delta'], 'UNCHANGED')
        self.assertEqual(sorted_f[2]['delta'], 'NEW')

    def test_different_files_tracked_independently(self):
        findings = [
            self._finding('unpinned-uses', 'aeon.yml', 10),
            self._finding('unpinned-uses', 'lint.yml', 10),
        ]
        tag_findings(findings, {('unpinned-uses', 'aeon.yml'): 1})
        aeon = next(f for f in findings if 'aeon' in f['file'])
        lint = next(f for f in findings if 'lint' in f['file'])
        self.assertEqual(aeon['delta'], 'UNCHANGED')
        self.assertEqual(lint['delta'], 'NEW')

    def test_directory_prefix_stripped_from_file(self):
        findings = [
            self._finding('artipacked', '.github/workflows/aeon.yml', 5),
        ]
        tag_findings(findings, {('artipacked', 'aeon.yml'): 1})
        self.assertEqual(findings[0]['delta'], 'UNCHANGED')

    def test_prior_exceeds_today_all_unchanged(self):
        findings = [self._finding('unpinned-uses', 'aeon.yml', 10)]
        tag_findings(findings, {('unpinned-uses', 'aeon.yml'): 5})
        self.assertEqual(findings[0]['delta'], 'UNCHANGED')

    def test_prior_zero_all_new(self):
        findings = [self._finding('unpinned-uses', 'aeon.yml', 10)]
        tag_findings(findings, {('unpinned-uses', 'aeon.yml'): 0})
        self.assertEqual(findings[0]['delta'], 'NEW')


if __name__ == '__main__':
    unittest.main(verbosity=2)
