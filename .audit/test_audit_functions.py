#!/usr/bin/env python3
"""
Unit tests for pure-function logic in classify.py, delta.py, and finalize.py.

Run: python .audit/test_audit_functions.py

Covers:
 - our_severity(): all five branches, including empty/uppercase confidence edge cases
 - make_fingerprint(): basename normalisation, snippet truncation at 60, whitespace collapse
 - fp_for(): basename normalisation, underscore-vs-space step names (delta.py adds both)
 - Calibration rules: secrets-outside-env High->Medium, unpinned-uses Critical->High
"""

import hashlib
import os
import re
import unittest


# ── Inline copies of the pure functions under test ───────────────────────────
# Production scripts (classify.py / delta.py / finalize.py) are not importable
# as modules; we inline the pure logic here so it can be tested in isolation.

def our_severity(f):
    """Copied verbatim from classify.py."""
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
    """Copied verbatim from classify.py."""
    short_rule = f['rule_id'].split('/')[-1]
    snip_key = re.sub(r'\s+', ' ', f['snippet'])[:60]
    file_short = os.path.basename(f['file'])
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


def fp_for(rule, fname, step):
    """Copied verbatim from delta.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Tests ────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    # Critical branch
    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_conf_case_insensitive(self):
        # confidence is .lower()'d — 'HIGH' must still yield Critical
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    # High branch — error with non-high confidence
    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_conf_is_high(self):
        # get() default of '' → not 'high' → second branch fires
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    # High branch — warning with high confidence
    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    # Medium branch
    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_low_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    # Low branch (catch-all)
    def test_note_level_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'unknown-future-level'}), 'Low')


class TestMakeFingerprint(unittest.TestCase):

    def _finding(self, **kwargs):
        base = {
            'rule_id': 'zizmor/template-injection',
            'file': '.github/workflows/aeon.yml',
            'snippet': 'echo "${{ github.event.inputs.msg }}"',
        }
        base.update(kwargs)
        return base

    def test_fingerprint_is_16_hex_chars(self):
        fp = make_fingerprint(self._finding())
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]+$')

    def test_fingerprint_is_deterministic(self):
        f = self._finding()
        self.assertEqual(make_fingerprint(f), make_fingerprint(f))

    def test_fingerprint_uses_basename_not_full_path(self):
        # Two different directories but same basename → identical fingerprint
        a = make_fingerprint(self._finding(file='dir/aeon.yml'))
        b = make_fingerprint(self._finding(file='other/dir/aeon.yml'))
        self.assertEqual(a, b)

    def test_fingerprint_differs_on_different_rule(self):
        a = make_fingerprint(self._finding(rule_id='zizmor/rule-a'))
        b = make_fingerprint(self._finding(rule_id='zizmor/rule-b'))
        self.assertNotEqual(a, b)

    def test_fingerprint_differs_on_different_file_basename(self):
        a = make_fingerprint(self._finding(file='aeon.yml'))
        b = make_fingerprint(self._finding(file='messages.yml'))
        self.assertNotEqual(a, b)

    def test_snippet_truncated_at_60(self):
        # Snippet of length 60 and 61 (differing only past the cut) → same fp
        a = make_fingerprint(self._finding(snippet='x' * 60))
        b = make_fingerprint(self._finding(snippet='x' * 60 + 'y'))
        self.assertEqual(a, b)

    def test_snippet_shorter_than_60_not_padded(self):
        a = make_fingerprint(self._finding(snippet='abc'))
        b = make_fingerprint(self._finding(snippet='abc' + ' ' * 57))
        # trailing spaces are part of the value — must differ
        self.assertNotEqual(a, b)

    def test_snippet_whitespace_normalised(self):
        # Tabs and multiple spaces collapse to single space
        a = make_fingerprint(self._finding(snippet='a  b\tc'))
        b = make_fingerprint(self._finding(snippet='a b c'))
        self.assertEqual(a, b)

    def test_rule_uses_part_after_last_slash(self):
        # 'zizmor/template-injection' and 'template-injection' both → short rule
        # 'template-injection', so fingerprints match.
        a = make_fingerprint(self._finding(rule_id='zizmor/template-injection'))
        b = make_fingerprint(self._finding(rule_id='template-injection'))
        self.assertEqual(a, b)


class TestFpFor(unittest.TestCase):
    """Tests for the fingerprint helper in delta.py."""

    def test_is_16_hex_chars(self):
        fp = fp_for('template-injection', '.github/workflows/aeon.yml', 'Setup')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]+$')

    def test_deterministic(self):
        args = ('template-injection', '.github/workflows/aeon.yml', 'Checkout code')
        self.assertEqual(fp_for(*args), fp_for(*args))

    def test_uses_basename_not_full_path(self):
        # delta.py strips to basename — full path and bare name must agree
        a = fp_for('rule', '.github/workflows/messages.yml', 'Run')
        b = fp_for('rule', 'messages.yml', 'Run')
        self.assertEqual(a, b)

    def test_step_underscore_and_space_produce_different_fps(self):
        # delta.py deliberately adds BOTH fp_for(…, step_with_space) and
        # fp_for(…, step_with_underscore) to the prior_fp_set because prior
        # audits stored "Setup_Node" while current audits use "Setup Node".
        # These must produce different values so both variants are needed.
        a = fp_for('rule', 'f.yml', 'Setup Node')
        b = fp_for('rule', 'f.yml', 'Setup_Node')
        self.assertNotEqual(a, b)

    def test_differs_on_different_rule(self):
        a = fp_for('rule-a', 'f.yml', 'Step')
        b = fp_for('rule-b', 'f.yml', 'Step')
        self.assertNotEqual(a, b)

    def test_differs_on_different_step(self):
        a = fp_for('rule', 'f.yml', 'Step A')
        b = fp_for('rule', 'f.yml', 'Step B')
        self.assertNotEqual(a, b)


class TestFinalizeCalibration(unittest.TestCase):
    """
    Inline the calibration rules from finalize.py and delta.py.
    Neither script is importable, so we replicate the logic here.
    """

    def _apply_finalize_calibration(self, findings):
        for f in findings:
            if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
                f['severity'] = 'Medium'
                f.setdefault('calibrated_notes', []).append(
                    'secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)'
                )
        return findings

    def _apply_delta_calibration(self, findings):
        for f in findings:
            if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
                f['severity'] = 'High'
                f['calibrated'] = True
        return findings

    # ── finalize.py calibration ──

    def test_secrets_outside_env_high_becomes_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        result = self._apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')
        self.assertIn('calibrated_notes', result[0])

    def test_secrets_outside_env_critical_not_touched(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Critical'}]
        result = self._apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Critical')
        self.assertNotIn('calibrated_notes', result[0])

    def test_secrets_outside_env_medium_not_touched(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        result = self._apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')
        self.assertNotIn('calibrated_notes', result[0])

    def test_other_rule_high_not_touched_by_finalize(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'High'}]
        result = self._apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertNotIn('calibrated_notes', result[0])

    # ── delta.py calibration ──

    def test_unpinned_uses_critical_becomes_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        result = self._apply_delta_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertTrue(result[0]['calibrated'])

    def test_unpinned_uses_high_not_touched(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        result = self._apply_delta_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertNotIn('calibrated', result[0])

    def test_other_rule_critical_not_touched_by_delta(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
        result = self._apply_delta_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Critical')
        self.assertNotIn('calibrated', result[0])


if __name__ == '__main__':
    unittest.main(verbosity=2)
