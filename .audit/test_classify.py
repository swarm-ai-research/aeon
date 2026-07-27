"""Unit tests for the severity classification, fingerprint, and calibration logic
shared across .audit/classify.py, .audit/extract_steps.py, and .audit/finalize.py.

The production scripts do file I/O on import, so the pure functions are
inlined here verbatim for testability. If the logic diverges, update these copies.

Run: python3 .audit/test_classify.py
"""

import hashlib
import os
import re
import unittest


# ── Inlined from classify.py / extract_steps.py ──────────────────────────────

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


def classify_fingerprint(rule_id, file_path, snippet):
    """Fingerprint scheme from classify.py: hash(short_rule|basename|snippet[:60])."""
    short_rule = rule_id.split('/')[-1]
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(file_path)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


def step_fingerprint(short_rule, file_path, step):
    """Fingerprint scheme from extract_steps.py: hash(short_rule|file|step)."""
    fp_src = f"{short_rule}|{file_path}|{step}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ── Inlined from finalize.py ──────────────────────────────────────────────────

def calibrate_finalize(findings):
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)'
            )
    return findings


# ── Inlined from parse_sarif.py (property fallback chain) ────────────────────

def extract_severity_prop(props):
    return (
        props.get('problem.severity')
        or props.get('zizmor/severity')
        or props.get('security-severity', '')
    )


# ─────────────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    # ── Critical path ──────────────────────────────────────────────────────

    def test_error_high_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_confidence_case_folded(self):
        # conf is .lower()-ed; uppercase variants should still reach 'high'
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

    # ── High path ──────────────────────────────────────────────────────────

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_confidence_key_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    # ── Medium path ────────────────────────────────────────────────────────

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_warning_missing_confidence_key_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    # ── Low path (else branch) ─────────────────────────────────────────────

    def test_note_high_confidence_is_low(self):
        # 'note' is not 'error' or 'warning', so falls through to Low
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_note_empty_confidence_is_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': ''}), 'Low')

    def test_note_missing_confidence_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({'level': '', 'confidence': 'high'}), 'Low')


class TestClassifyFingerprint(unittest.TestCase):

    def test_rule_without_slash_uses_full_id(self):
        fp = classify_fingerprint('artipacked', 'workflows/deploy.yml', 'snip')
        expected = hashlib.sha256(b'artipacked|deploy.yml|snip').hexdigest()[:16]
        self.assertEqual(fp, expected)

    def test_rule_with_slash_uses_last_segment(self):
        fp_namespaced = classify_fingerprint('zizmor/artipacked', 'workflows/deploy.yml', 'snip')
        fp_bare = classify_fingerprint('artipacked', 'workflows/deploy.yml', 'snip')
        self.assertEqual(fp_namespaced, fp_bare)

    def test_snippet_whitespace_normalized(self):
        fp_tabs = classify_fingerprint('rule', 'file.yml', 'a\t\tb')
        fp_spaces = classify_fingerprint('rule', 'file.yml', 'a b')
        self.assertEqual(fp_tabs, fp_spaces)

    def test_snippet_newlines_normalized(self):
        fp_newline = classify_fingerprint('rule', 'file.yml', 'a\nb')
        fp_space = classify_fingerprint('rule', 'file.yml', 'a b')
        self.assertEqual(fp_newline, fp_space)

    def test_snippet_truncated_at_60_chars(self):
        fp_long = classify_fingerprint('rule', 'file.yml', 'x' * 100)
        fp_60 = classify_fingerprint('rule', 'file.yml', 'x' * 60)
        self.assertEqual(fp_long, fp_60)

    def test_snippet_not_truncated_below_60(self):
        fp_59 = classify_fingerprint('rule', 'file.yml', 'x' * 59)
        fp_60 = classify_fingerprint('rule', 'file.yml', 'x' * 60)
        self.assertNotEqual(fp_59, fp_60)

    def test_fingerprint_uses_basename_only(self):
        fp_full = classify_fingerprint('rule', '.github/workflows/deploy.yml', 'snip')
        fp_base = classify_fingerprint('rule', 'deploy.yml', 'snip')
        self.assertEqual(fp_full, fp_base)

    def test_fingerprint_is_16_hex_chars(self):
        fp = classify_fingerprint('rule', 'file.yml', 'snip')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')

    def test_different_rules_produce_different_fingerprints(self):
        fp1 = classify_fingerprint('artipacked', 'file.yml', 'snip')
        fp2 = classify_fingerprint('unpinned-uses', 'file.yml', 'snip')
        self.assertNotEqual(fp1, fp2)


class TestStepFingerprint(unittest.TestCase):

    def test_fingerprint_uses_full_file_path(self):
        # extract_steps.py uses full path, not basename
        fp_full = step_fingerprint('rule', '.github/workflows/deploy.yml', 'Setup Node')
        fp_base = step_fingerprint('rule', 'deploy.yml', 'Setup Node')
        self.assertNotEqual(fp_full, fp_base)

    def test_fingerprint_is_16_hex_chars(self):
        fp = step_fingerprint('artipacked', '.github/workflows/ci.yml', 'Checkout')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')


class TestCalibrateFinalize(unittest.TestCase):

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        calibrate_finalize(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')

    def test_calibrated_note_appended(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        calibrate_finalize(findings)
        self.assertIn('calibrated_notes', findings[0])
        self.assertEqual(len(findings[0]['calibrated_notes']), 1)

    def test_secrets_outside_env_medium_unchanged(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        calibrate_finalize(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')
        self.assertNotIn('calibrated_notes', findings[0])

    def test_secrets_outside_env_critical_not_downgraded(self):
        # Only 'High' is touched; Critical is left alone
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Critical'}]
        calibrate_finalize(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')

    def test_secrets_outside_env_low_not_downgraded(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Low'}]
        calibrate_finalize(findings)
        self.assertEqual(findings[0]['severity'], 'Low')

    def test_other_rule_high_not_downgraded(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        calibrate_finalize(findings)
        self.assertEqual(findings[0]['severity'], 'High')

    def test_mixed_findings_only_target_downgraded(self):
        findings = [
            {'short_rule': 'secrets-outside-env', 'severity': 'High'},
            {'short_rule': 'unpinned-uses', 'severity': 'High'},
            {'short_rule': 'secrets-outside-env', 'severity': 'Critical'},
        ]
        calibrate_finalize(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')
        self.assertEqual(findings[1]['severity'], 'High')
        self.assertEqual(findings[2]['severity'], 'Critical')


class TestExtractSeverityProp(unittest.TestCase):
    """Tests the fallback chain used in parse_sarif.py to read severity from SARIF properties."""

    def test_problem_severity_wins(self):
        props = {'problem.severity': 'high', 'zizmor/severity': 'medium', 'security-severity': 'low'}
        self.assertEqual(extract_severity_prop(props), 'high')

    def test_falls_through_to_zizmor_severity_when_problem_absent(self):
        props = {'zizmor/severity': 'medium', 'security-severity': 'low'}
        self.assertEqual(extract_severity_prop(props), 'medium')

    def test_falls_through_to_security_severity_when_both_absent(self):
        props = {'security-severity': '7.5'}
        self.assertEqual(extract_severity_prop(props), '7.5')

    def test_empty_string_problem_severity_falls_through(self):
        # Empty string is falsy; the 'or' chain should skip to the next key
        props = {'problem.severity': '', 'zizmor/severity': 'medium'}
        self.assertEqual(extract_severity_prop(props), 'medium')

    def test_all_absent_returns_empty_string(self):
        self.assertEqual(extract_severity_prop({}), '')

    def test_none_value_falls_through(self):
        # .get() returns None for a missing key; None is falsy
        props = {'problem.severity': None, 'zizmor/severity': 'high'}
        self.assertEqual(extract_severity_prop(props), 'high')


if __name__ == '__main__':
    unittest.main()
