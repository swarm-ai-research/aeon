"""Tests for pure logic in .audit/ scripts.

Run: python3 .audit/test_audit_logic.py

Functions are inlined here rather than imported because the source scripts
execute side-effecting code at module scope (file I/O, print).
"""

import hashlib
import os
import re
import unittest


# ── our_severity() — from classify.py ────────────────────────────────────────

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


class TestOurSeverity(unittest.TestCase):

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_low_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_missing_conf_is_high(self):
        # Missing key falls through to the bare 'error' branch, not Critical
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_no_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_is_low(self):
        # else-branch: anything other than error/warning maps to Low
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info', 'confidence': 'high'}), 'Low')

    def test_confidence_case_insensitive(self):
        # .lower() is applied, so 'HIGH' and 'High' must both trigger Critical
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')


# ── short_rule extraction — from classify.py ─────────────────────────────────

def short_rule(rule_id):
    return rule_id.split('/')[-1]


class TestShortRule(unittest.TestCase):

    def test_slash_prefix_stripped(self):
        self.assertEqual(short_rule('zizmor/secrets-outside-env'), 'secrets-outside-env')

    def test_no_slash_returns_full_string(self):
        # Edge case: rule_id contains no slash — split('/') still returns a
        # one-element list so [-1] is the original string.
        self.assertEqual(short_rule('unpinned-uses'), 'unpinned-uses')

    def test_multiple_slashes_returns_last_segment(self):
        self.assertEqual(short_rule('org/repo/some-rule'), 'some-rule')


# ── fingerprint (classify.py) — whitespace normalisation & length cap ─────────

def classify_fingerprint(short_rule_val, file_path, snippet):
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(file_path)
    fp_src = f"{short_rule_val}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


class TestClassifyFingerprint(unittest.TestCase):

    def test_deterministic(self):
        a = classify_fingerprint('foo', 'dir/bar.yml', 'some snippet')
        b = classify_fingerprint('foo', 'dir/bar.yml', 'some snippet')
        self.assertEqual(a, b)

    def test_length_is_16_hex(self):
        fp = classify_fingerprint('rule', 'file.yml', 'code')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')

    def test_whitespace_normalised_before_hashing(self):
        # Newlines and multiple spaces in the snippet collapse to single space,
        # so both variants must produce the same fingerprint.
        fp1 = classify_fingerprint('rule', 'f.yml', 'a  b\tc')
        fp2 = classify_fingerprint('rule', 'f.yml', 'a b c')
        self.assertEqual(fp1, fp2)

    def test_snippet_truncated_at_60_chars(self):
        long_snip = 'x' * 100
        short_snip = 'x' * 60
        self.assertEqual(
            classify_fingerprint('r', 'f.yml', long_snip),
            classify_fingerprint('r', 'f.yml', short_snip),
        )

    def test_basename_used_not_full_path(self):
        fp1 = classify_fingerprint('rule', '.github/workflows/aeon.yml', 'code')
        fp2 = classify_fingerprint('rule', 'aeon.yml', 'code')
        self.assertEqual(fp1, fp2)

    def test_different_rules_differ(self):
        fp1 = classify_fingerprint('rule-a', 'f.yml', 'code')
        fp2 = classify_fingerprint('rule-b', 'f.yml', 'code')
        self.assertNotEqual(fp1, fp2)


# ── fp() — from gen_trailer.py ───────────────────────────────────────────────

def gen_trailer_fp(rule, fname, step):
    s = f"{rule}|{os.path.basename(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class TestGenTrailerFp(unittest.TestCase):

    def test_deterministic(self):
        self.assertEqual(
            gen_trailer_fp('rule', 'aeon.yml', 'Run step'),
            gen_trailer_fp('rule', 'aeon.yml', 'Run step'),
        )

    def test_spaces_become_underscores(self):
        # 'Run step' and 'Run_step' must hash identically because spaces in the
        # step name are replaced with underscores before hashing.
        fp_spaces = gen_trailer_fp('rule', 'f.yml', 'Run step')
        fp_underscores = gen_trailer_fp('rule', 'f.yml', 'Run_step')
        self.assertEqual(fp_spaces, fp_underscores)

    def test_step_without_spaces_unchanged(self):
        fp1 = gen_trailer_fp('rule', 'f.yml', 'Checkout')
        fp2 = gen_trailer_fp('rule', 'f.yml', 'Checkout')
        self.assertEqual(fp1, fp2)

    def test_length_and_hex(self):
        fp = gen_trailer_fp('rule', 'f.yml', 'step')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')

    def test_basename_used(self):
        fp1 = gen_trailer_fp('rule', '.github/workflows/aeon.yml', 'step')
        fp2 = gen_trailer_fp('rule', 'aeon.yml', 'step')
        self.assertEqual(fp1, fp2)


# ── SARIF locations absent edge case — from parse_sarif.py ───────────────────

def parse_sarif_result(r):
    """Mirrors the per-result parsing block in parse_sarif.py."""
    rule_id = r.get('ruleId', '?')
    level = r.get('level', 'note')
    message = r.get('message', {}).get('text', '')
    props = r.get('properties', {})
    sev = props.get('problem.severity') or props.get('zizmor/severity') or props.get('security-severity', '')
    conf = props.get('zizmor/confidence', '')
    locs = r.get('locations', [])
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
    return {
        'rule_id': rule_id,
        'level': level,
        'severity_zizmor': sev,
        'confidence': conf,
        'message': message,
        'file': uri,
        'line': line,
        'snippet': snippet[:200],
    }


class TestParseSarifResult(unittest.TestCase):

    def test_no_locations_defaults_to_empty(self):
        result = parse_sarif_result({'ruleId': 'foo', 'level': 'warning'})
        self.assertEqual(result['file'], '')
        self.assertEqual(result['line'], 0)
        self.assertEqual(result['snippet'], '')

    def test_missing_rule_id_defaults_to_question_mark(self):
        result = parse_sarif_result({'level': 'error'})
        self.assertEqual(result['rule_id'], '?')

    def test_missing_level_defaults_to_note(self):
        result = parse_sarif_result({'ruleId': 'bar'})
        self.assertEqual(result['level'], 'note')

    def test_snippet_truncated_at_200(self):
        long = 'a' * 300
        r = {
            'ruleId': 'r', 'level': 'note',
            'locations': [{'physicalLocation': {
                'artifactLocation': {'uri': 'f.yml'},
                'region': {'startLine': 1, 'snippet': {'text': long}},
            }}],
        }
        self.assertEqual(len(parse_sarif_result(r)['snippet']), 200)

    def test_severity_property_priority(self):
        # 'problem.severity' wins over 'zizmor/severity'
        props = {'problem.severity': 'high', 'zizmor/severity': 'low'}
        result = parse_sarif_result({'ruleId': 'r', 'level': 'note', 'properties': props})
        self.assertEqual(result['severity_zizmor'], 'high')

    def test_severity_falls_back_to_zizmor_severity(self):
        props = {'zizmor/severity': 'medium'}
        result = parse_sarif_result({'ruleId': 'r', 'level': 'note', 'properties': props})
        self.assertEqual(result['severity_zizmor'], 'medium')

    def test_full_location_parsed(self):
        r = {
            'ruleId': 'zizmor/foo', 'level': 'error',
            'locations': [{'physicalLocation': {
                'artifactLocation': {'uri': '.github/workflows/aeon.yml'},
                'region': {'startLine': 42, 'snippet': {'text': 'run: echo hi'}},
            }}],
        }
        result = parse_sarif_result(r)
        self.assertEqual(result['file'], '.github/workflows/aeon.yml')
        self.assertEqual(result['line'], 42)
        self.assertEqual(result['snippet'], 'run: echo hi')


if __name__ == '__main__':
    unittest.main()
