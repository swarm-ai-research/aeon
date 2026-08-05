"""
Tests for the classification and fingerprinting logic in classify.py and delta.py.

The scripts can't be imported cleanly (they read files at module level), so the
core functions are reproduced here and tested in isolation.  Any change to the
logic in classify.py / delta.py / finalize.py should be reflected here.

Run: python3 .audit/test_classify.py
"""

import hashlib
import os
import re
import unittest


# ---------------------------------------------------------------------------
# Logic copied from classify.py
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


def make_fingerprint(rule_id, uri, snippet):
    short_rule = rule_id.split('/')[-1]
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(uri)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Calibration helpers from delta.py / finalize.py
# ---------------------------------------------------------------------------

def apply_delta_calibration(finding):
    """Reproduce the unpinned-uses Critical→High downgrade from delta.py."""
    f = dict(finding)
    if f.get('short_rule') == 'unpinned-uses' and f.get('severity') == 'Critical':
        f['severity'] = 'High'
        f['calibrated'] = True
    return f


def apply_finalize_calibration(finding):
    """Reproduce the secrets-outside-env High→Medium downgrade from finalize.py."""
    f = dict(finding)
    if f.get('short_rule') == 'secrets-outside-env' and f.get('severity') == 'High':
        f['severity'] = 'Medium'
        f.setdefault('calibrated_notes', []).append(
            'secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)'
        )
    return f


# ---------------------------------------------------------------------------
# Tests — our_severity()
# ---------------------------------------------------------------------------

class TestOurSeverity(unittest.TestCase):

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        # Second branch: error without high confidence → High
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_empty_confidence_is_high(self):
        # Missing confidence field still falls to error→High
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_confidence_key_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        # Third branch: warning + high confidence → High (distinct from error)
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_confidence_is_medium(self):
        # Fourth branch: warning without high confidence → Medium
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_note_level_is_low(self):
        # Fifth branch (default): note → Low — uncovered before this test
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        # Anything that isn't error/warning/note falls through to Low
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')
        self.assertEqual(our_severity({'level': '', 'confidence': 'high'}), 'Low')

    def test_confidence_matching_is_case_insensitive(self):
        # The function lowercases conf before comparing
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')


# ---------------------------------------------------------------------------
# Tests — make_fingerprint()
# ---------------------------------------------------------------------------

class TestMakeFingerprint(unittest.TestCase):

    def test_output_is_16_lowercase_hex_chars(self):
        fp = make_fingerprint('zizmor/template-injection', '.github/workflows/ci.yml', 'echo ${{ inputs.msg }}')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')

    def test_rule_id_uses_last_slash_segment(self):
        # "zizmor/template-injection" and "template-injection" must hash the same
        fp1 = make_fingerprint('template-injection', 'ci.yml', 'snippet')
        fp2 = make_fingerprint('zizmor/template-injection', 'ci.yml', 'snippet')
        self.assertEqual(fp1, fp2)

    def test_only_basename_of_uri_used(self):
        fp1 = make_fingerprint('rule', '.github/workflows/messages.yml', 'snippet')
        fp2 = make_fingerprint('rule', 'messages.yml', 'snippet')
        self.assertEqual(fp1, fp2)

    def test_long_snippet_truncated_at_60_chars(self):
        # Snippet longer than 60 chars must produce the same fingerprint as the
        # 60-char prefix — the tail is dropped before hashing.
        long = 'a' * 200
        fp1 = make_fingerprint('rule', 'ci.yml', long)
        fp2 = make_fingerprint('rule', 'ci.yml', 'a' * 60)
        self.assertEqual(fp1, fp2)

    def test_snippet_longer_than_60_differs_from_shorter_prefix(self):
        # Verify truncation is meaningful: 59 chars ≠ 60 chars
        fp59 = make_fingerprint('rule', 'ci.yml', 'a' * 59)
        fp60 = make_fingerprint('rule', 'ci.yml', 'a' * 60)
        self.assertNotEqual(fp59, fp60)

    def test_whitespace_normalized_before_hashing(self):
        # Multiple spaces, tabs, and newlines all collapse to a single space
        fp1 = make_fingerprint('rule', 'ci.yml', 'echo  hello\n  world')
        fp2 = make_fingerprint('rule', 'ci.yml', 'echo hello world')
        self.assertEqual(fp1, fp2)

    def test_empty_snippet_is_valid(self):
        fp = make_fingerprint('rule', 'ci.yml', '')
        self.assertEqual(len(fp), 16)

    def test_different_rules_produce_different_fingerprints(self):
        fp1 = make_fingerprint('rule-a', 'ci.yml', 'snippet')
        fp2 = make_fingerprint('rule-b', 'ci.yml', 'snippet')
        self.assertNotEqual(fp1, fp2)

    def test_different_files_produce_different_fingerprints(self):
        fp1 = make_fingerprint('rule', 'ci.yml', 'snippet')
        fp2 = make_fingerprint('rule', 'deploy.yml', 'snippet')
        self.assertNotEqual(fp1, fp2)

    def test_deterministic_across_calls(self):
        args = ('zizmor/template-injection', '.github/workflows/aeon.yml', '${{ github.event.client_payload.message }}')
        self.assertEqual(make_fingerprint(*args), make_fingerprint(*args))


# ---------------------------------------------------------------------------
# Tests — calibration overrides (delta.py + finalize.py)
# ---------------------------------------------------------------------------

class TestCalibrationOverrides(unittest.TestCase):

    def test_unpinned_uses_critical_downgraded_to_high(self):
        result = apply_delta_calibration({'short_rule': 'unpinned-uses', 'severity': 'Critical'})
        self.assertEqual(result['severity'], 'High')
        self.assertTrue(result.get('calibrated'))

    def test_unpinned_uses_already_high_not_changed(self):
        result = apply_delta_calibration({'short_rule': 'unpinned-uses', 'severity': 'High'})
        self.assertEqual(result['severity'], 'High')
        self.assertFalse(result.get('calibrated', False))

    def test_other_critical_rules_not_downgraded(self):
        result = apply_delta_calibration({'short_rule': 'template-injection', 'severity': 'Critical'})
        self.assertEqual(result['severity'], 'Critical')
        self.assertFalse(result.get('calibrated', False))

    def test_unpinned_uses_medium_not_changed(self):
        result = apply_delta_calibration({'short_rule': 'unpinned-uses', 'severity': 'Medium'})
        self.assertEqual(result['severity'], 'Medium')

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        result = apply_finalize_calibration({'short_rule': 'secrets-outside-env', 'severity': 'High'})
        self.assertEqual(result['severity'], 'Medium')
        self.assertTrue(result.get('calibrated_notes'))

    def test_secrets_outside_env_medium_not_double_downgraded(self):
        result = apply_finalize_calibration({'short_rule': 'secrets-outside-env', 'severity': 'Medium'})
        self.assertEqual(result['severity'], 'Medium')
        self.assertFalse(result.get('calibrated_notes'))

    def test_other_high_rules_not_downgraded_by_finalize(self):
        result = apply_finalize_calibration({'short_rule': 'template-injection', 'severity': 'High'})
        self.assertEqual(result['severity'], 'High')
        self.assertFalse(result.get('calibrated_notes'))

    def test_calibration_does_not_mutate_input(self):
        original = {'short_rule': 'unpinned-uses', 'severity': 'Critical'}
        apply_delta_calibration(original)
        self.assertEqual(original['severity'], 'Critical')


if __name__ == '__main__':
    unittest.main(verbosity=2)
