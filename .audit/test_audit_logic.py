"""
Unit tests for audit pipeline logic extracted from classify.py, delta.py, delta2.py,
and parse_sarif.py. Run with: python3 .audit/test_audit_logic.py

These tests cover branches that are otherwise never exercised since the scripts only
run in the context of a full workflow-security-audit skill run.
"""

import unittest
import hashlib
import os
import re


# ── Logic replicated from classify.py ──────────────────────────────────────

def our_severity(f):
    """Classify a finding dict into Critical/High/Medium/Low."""
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


def make_fingerprint(short_rule, file_uri, snippet):
    """Replicate classify.py fingerprint construction."""
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(file_uri)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ── Logic replicated from parse_sarif.py ───────────────────────────────────

def extract_severity_prop(props):
    """Replicate the three-way fallback chain for severity properties."""
    return (
        props.get('problem.severity')
        or props.get('zizmor/severity')
        or props.get('security-severity', '')
    )


def parse_location(locs):
    """Replicate the locs-present / locs-absent branch from parse_sarif.py."""
    if locs:
        phys = locs[0].get('physicalLocation', {})
        uri = phys.get('artifactLocation', {}).get('uri', '')
        region = phys.get('region', {})
        line = region.get('startLine', 0)
        snippet = region.get('snippet', {}).get('text', '')
    else:
        uri = ''
        line = 0
        snippet = ''
    return uri, line, snippet


# ── Logic replicated from delta.py / delta2.py ─────────────────────────────

def apply_calibration(findings):
    """Replicate the unpinned-uses Critical→High calibration."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


def apply_finalize_calibration(findings):
    """Replicate finalize.py's secrets-outside-env High→Medium downgrade."""
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)'
            )
    return findings


def aggregate_files_is_empty(files_str):
    """Replicate the delta2.py guard: skip aggregates with empty file list."""
    files = files_str.split(',')
    return not files or files == ['']


def template_injection_note_guard(agg_rule, finding_severity):
    """
    Replicate delta.py's guard: for 'template-injection-note' aggregates, only
    Low-severity findings are considered UNCHANGED. Higher-severity template-injection
    findings should not be suppressed as UNCHANGED.
    """
    if agg_rule == 'template-injection-note' and finding_severity != 'Low':
        return True   # skip — do NOT mark this finding as UNCHANGED
    return False


# ── Tests ──────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    def test_error_high_confidence_is_critical(self):
        f = {'level': 'error', 'confidence': 'high'}
        self.assertEqual(our_severity(f), 'Critical')

    def test_error_medium_confidence_is_high(self):
        f = {'level': 'error', 'confidence': 'medium'}
        self.assertEqual(our_severity(f), 'High')

    def test_error_low_confidence_is_high(self):
        f = {'level': 'error', 'confidence': 'low'}
        self.assertEqual(our_severity(f), 'High')

    def test_error_no_confidence_is_high(self):
        f = {'level': 'error'}
        self.assertEqual(our_severity(f), 'High')

    def test_warning_high_confidence_is_high(self):
        f = {'level': 'warning', 'confidence': 'high'}
        self.assertEqual(our_severity(f), 'High')

    def test_warning_medium_confidence_is_medium(self):
        f = {'level': 'warning', 'confidence': 'medium'}
        self.assertEqual(our_severity(f), 'Medium')

    def test_warning_low_confidence_is_medium(self):
        f = {'level': 'warning', 'confidence': 'low'}
        self.assertEqual(our_severity(f), 'Medium')

    def test_warning_no_confidence_is_medium(self):
        f = {'level': 'warning'}
        self.assertEqual(our_severity(f), 'Medium')

    def test_note_is_low(self):
        f = {'level': 'note', 'confidence': 'high'}
        self.assertEqual(our_severity(f), 'Low')

    def test_unknown_level_is_low(self):
        f = {'level': 'info', 'confidence': 'high'}
        self.assertEqual(our_severity(f), 'Low')

    def test_confidence_comparison_is_case_insensitive(self):
        # confidence is lowercased before comparison
        f = {'level': 'error', 'confidence': 'HIGH'}
        self.assertEqual(our_severity(f), 'Critical')


class TestSeverityPropertyFallback(unittest.TestCase):

    def test_problem_severity_takes_precedence(self):
        props = {
            'problem.severity': 'critical',
            'zizmor/severity': 'high',
            'security-severity': 'medium',
        }
        self.assertEqual(extract_severity_prop(props), 'critical')

    def test_falls_back_to_zizmor_severity(self):
        props = {
            'problem.severity': '',   # falsy → skip
            'zizmor/severity': 'high',
            'security-severity': 'medium',
        }
        self.assertEqual(extract_severity_prop(props), 'high')

    def test_falls_back_to_security_severity(self):
        props = {
            'zizmor/severity': '',    # falsy → skip
            'security-severity': '7.5',
        }
        self.assertEqual(extract_severity_prop(props), '7.5')

    def test_all_missing_returns_empty_string(self):
        props = {}
        self.assertEqual(extract_severity_prop(props), '')

    def test_none_value_triggers_fallback(self):
        props = {
            'problem.severity': None,
            'zizmor/severity': 'medium',
        }
        self.assertEqual(extract_severity_prop(props), 'medium')


class TestParseLocation(unittest.TestCase):

    def test_empty_locs_returns_defaults(self):
        uri, line, snippet = parse_location([])
        self.assertEqual(uri, '')
        self.assertEqual(line, 0)
        self.assertEqual(snippet, '')

    def test_none_equivalent_locs_returns_defaults(self):
        uri, line, snippet = parse_location(None)
        self.assertEqual(uri, '')
        self.assertEqual(line, 0)
        self.assertEqual(snippet, '')

    def test_full_location_extracted(self):
        locs = [{
            'physicalLocation': {
                'artifactLocation': {'uri': '.github/workflows/aeon.yml'},
                'region': {
                    'startLine': 42,
                    'snippet': {'text': 'run: echo ${{ github.event.head_commit.message }}'},
                },
            }
        }]
        uri, line, snippet = parse_location(locs)
        self.assertEqual(uri, '.github/workflows/aeon.yml')
        self.assertEqual(line, 42)
        self.assertIn('echo', snippet)

    def test_missing_region_keys_default(self):
        locs = [{'physicalLocation': {'artifactLocation': {'uri': 'foo.yml'}}}]
        uri, line, snippet = parse_location(locs)
        self.assertEqual(uri, 'foo.yml')
        self.assertEqual(line, 0)
        self.assertEqual(snippet, '')


class TestCalibration(unittest.TestCase):

    def test_unpinned_uses_critical_downgraded_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertTrue(findings[0].get('calibrated'))

    def test_unpinned_uses_already_high_unchanged(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertNotIn('calibrated', findings[0])

    def test_other_rule_critical_not_downgraded(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')
        self.assertNotIn('calibrated', findings[0])

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')
        self.assertIn('calibrated_notes', findings[0])

    def test_secrets_outside_env_medium_unchanged(self):
        findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
        apply_finalize_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Medium')
        self.assertNotIn('calibrated_notes', findings[0])


class TestAggregateEdgeCases(unittest.TestCase):

    def test_empty_files_string_detected(self):
        self.assertTrue(aggregate_files_is_empty(''))

    def test_non_empty_files_not_skipped(self):
        self.assertFalse(aggregate_files_is_empty('aeon.yml,lint.yml'))

    def test_single_file_not_skipped(self):
        self.assertFalse(aggregate_files_is_empty('aeon.yml'))

    def test_template_injection_note_skips_non_low(self):
        self.assertTrue(template_injection_note_guard('template-injection-note', 'High'))
        self.assertTrue(template_injection_note_guard('template-injection-note', 'Critical'))
        self.assertTrue(template_injection_note_guard('template-injection-note', 'Medium'))

    def test_template_injection_note_allows_low(self):
        self.assertFalse(template_injection_note_guard('template-injection-note', 'Low'))

    def test_other_aggregate_rule_never_skipped(self):
        self.assertFalse(template_injection_note_guard('secrets-outside-env', 'High'))
        self.assertFalse(template_injection_note_guard('unpinned-uses', 'Critical'))


class TestFingerprintStability(unittest.TestCase):

    def test_same_inputs_same_fingerprint(self):
        fp1 = make_fingerprint('template-injection', '.github/workflows/aeon.yml', 'run: echo $X')
        fp2 = make_fingerprint('template-injection', '.github/workflows/aeon.yml', 'run: echo $X')
        self.assertEqual(fp1, fp2)

    def test_different_rule_different_fingerprint(self):
        fp1 = make_fingerprint('template-injection', 'aeon.yml', 'run: echo $X')
        fp2 = make_fingerprint('unpinned-uses', 'aeon.yml', 'run: echo $X')
        self.assertNotEqual(fp1, fp2)

    def test_fingerprint_is_16_hex_chars(self):
        fp = make_fingerprint('artipacked', 'lint.yml', 'uses: actions/checkout@v3')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_basename_only_used_not_full_path(self):
        # Fingerprint should be based on basename, not the full URI, so two findings
        # with the same basename but different directory paths get the same fingerprint.
        fp_full = make_fingerprint('artipacked', '.github/workflows/aeon.yml', 'step')
        fp_base = make_fingerprint('artipacked', 'aeon.yml', 'step')
        self.assertEqual(fp_full, fp_base)

    def test_whitespace_normalised_in_snippet(self):
        fp1 = make_fingerprint('rule', 'f.yml', 'a  b\tc')
        fp2 = make_fingerprint('rule', 'f.yml', 'a b c')
        self.assertEqual(fp1, fp2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
