"""
Unit tests for pure logic extracted from the audit pipeline scripts.

Run: python -m pytest .audit/test_audit_logic.py -v
  or: python .audit/test_audit_logic.py
"""

import hashlib
import os
import sys
import unittest


# ── Pure functions copied verbatim from classify.py ──────────────────────────

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


def classify_short_rule(rule_id):
    return rule_id.split('/')[-1]


# ── Pure functions copied verbatim from gen_trailer.py ───────────────────────

def fp(rule, fname, step):
    s = f"{rule}|{os.path.basename(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Pure functions copied verbatim from delta.py ─────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Calibration logic from finalize.py ───────────────────────────────────────

def apply_finalize_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium'
            )
    return findings


# ── Calibration logic from delta.py / delta2.py ──────────────────────────────

def apply_unpinned_uses_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


# ─────────────────────────────────────────────────────────────────────────────


class TestOurSeverity(unittest.TestCase):
    def _f(self, level, confidence=''):
        return {'level': level, 'confidence': confidence}

    def test_error_high_is_critical(self):
        self.assertEqual(our_severity(self._f('error', 'high')), 'Critical')

    def test_error_high_case_insensitive(self):
        self.assertEqual(our_severity(self._f('error', 'High')), 'Critical')

    def test_error_medium_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'medium')), 'High')

    def test_error_low_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'low')), 'High')

    def test_error_no_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error')), 'High')

    def test_warning_high_is_high(self):
        self.assertEqual(our_severity(self._f('warning', 'high')), 'High')

    def test_warning_medium_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'medium')), 'Medium')

    def test_warning_low_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'low')), 'Medium')

    def test_warning_no_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning')), 'Medium')

    def test_note_is_low(self):
        self.assertEqual(our_severity(self._f('note')), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity(self._f('info')), 'Low')


class TestShortRule(unittest.TestCase):
    def test_no_slash(self):
        self.assertEqual(classify_short_rule('unpinned-uses'), 'unpinned-uses')

    def test_one_slash(self):
        self.assertEqual(classify_short_rule('zizmor/unpinned-uses'), 'unpinned-uses')

    def test_multiple_slashes(self):
        self.assertEqual(classify_short_rule('org/tool/rule-name'), 'rule-name')

    def test_empty_string(self):
        self.assertEqual(classify_short_rule(''), '')


class TestFingerprintFunctions(unittest.TestCase):
    """fp() and fp_for() must be 16-char lowercase hex and deterministic."""

    def test_fp_length(self):
        result = fp('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        self.assertEqual(len(result), 16)

    def test_fp_hex(self):
        result = fp('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_fp_deterministic(self):
        a = fp('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        b = fp('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        self.assertEqual(a, b)

    def test_fp_uses_basename(self):
        result_abs = fp('rule', '/long/path/.github/workflows/ci.yml', 'step')
        result_rel = fp('rule', '.github/workflows/ci.yml', 'step')
        result_base = fp('rule', 'ci.yml', 'step')
        self.assertEqual(result_abs, result_base)
        self.assertEqual(result_rel, result_base)

    def test_fp_spaces_replaced_by_underscores(self):
        with_space = fp('rule', 'ci.yml', 'Setup Node')
        with_underscore = fp('rule', 'ci.yml', 'Setup_Node')
        # gen_trailer.fp replaces spaces → underscores before hashing
        self.assertEqual(with_space, with_underscore)

    def test_fp_for_length(self):
        result = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        self.assertEqual(len(result), 16)

    def test_fp_for_hex(self):
        result = fp_for('rule', 'ci.yml', 'step')
        self.assertTrue(all(c in '0123456789abcdef' for c in result))

    def test_fp_for_deterministic(self):
        a = fp_for('rule', 'ci.yml', 'step')
        b = fp_for('rule', 'ci.yml', 'step')
        self.assertEqual(a, b)

    def test_fp_for_uses_basename(self):
        r1 = fp_for('rule', '/a/b/c.yml', 'step')
        r2 = fp_for('rule', 'c.yml', 'step')
        self.assertEqual(r1, r2)

    def test_fp_vs_fp_for_differ_on_spaces(self):
        # fp() normalises spaces; fp_for() does NOT — they can diverge on the same step
        result_fp = fp('rule', 'ci.yml', 'Setup Node')
        result_fp_for = fp_for('rule', 'ci.yml', 'Setup Node')
        # fp_for keeps the space, fp converts it; values differ
        self.assertNotEqual(result_fp, result_fp_for)

    def test_different_rules_give_different_fps(self):
        a = fp('rule-a', 'ci.yml', 'step')
        b = fp('rule-b', 'ci.yml', 'step')
        self.assertNotEqual(a, b)

    def test_different_files_give_different_fps(self):
        a = fp('rule', 'ci.yml', 'step')
        b = fp('rule', 'deploy.yml', 'step')
        self.assertNotEqual(a, b)


class TestFinalizeCalibration(unittest.TestCase):
    def _finding(self, short_rule, severity):
        return {'short_rule': short_rule, 'severity': severity}

    def test_secrets_outside_env_high_becomes_medium(self):
        findings = [self._finding('secrets-outside-env', 'High')]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')

    def test_secrets_outside_env_high_gets_calibrated_note(self):
        findings = [self._finding('secrets-outside-env', 'High')]
        result = apply_finalize_calibration(findings)
        self.assertIn('calibrated_notes', result[0])
        self.assertTrue(len(result[0]['calibrated_notes']) > 0)

    def test_secrets_outside_env_critical_unchanged(self):
        findings = [self._finding('secrets-outside-env', 'Critical')]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Critical')

    def test_secrets_outside_env_medium_unchanged(self):
        findings = [self._finding('secrets-outside-env', 'Medium')]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')

    def test_other_rule_high_unchanged(self):
        findings = [self._finding('unpinned-uses', 'High')]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')

    def test_multiple_findings_only_matching_downgraded(self):
        findings = [
            self._finding('secrets-outside-env', 'High'),
            self._finding('unpinned-uses', 'High'),
            self._finding('secrets-outside-env', 'Medium'),
        ]
        result = apply_finalize_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Medium')
        self.assertEqual(result[1]['severity'], 'High')
        self.assertEqual(result[2]['severity'], 'Medium')


class TestUnpinnedUsesCalibration(unittest.TestCase):
    def _finding(self, short_rule, severity):
        return {'short_rule': short_rule, 'severity': severity}

    def test_unpinned_uses_critical_becomes_high(self):
        findings = [self._finding('unpinned-uses', 'Critical')]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertTrue(result[0].get('calibrated'))

    def test_unpinned_uses_high_unchanged(self):
        findings = [self._finding('unpinned-uses', 'High')]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertNotIn('calibrated', result[0])

    def test_other_rule_critical_unchanged(self):
        findings = [self._finding('artipacked', 'Critical')]
        result = apply_unpinned_uses_calibration(findings)
        self.assertEqual(result[0]['severity'], 'Critical')


if __name__ == '__main__':
    unittest.main(verbosity=2)
