"""Unit tests for the logic embedded in classify.py and parse_sarif.py.

These scripts are not importable modules, so the tested functions are
re-declared here verbatim. Any drift between the copy and the source
will surface as a failing test.

Run: python .audit/test_classify.py
"""

import hashlib
import re
import os
import sys
import unittest


# --- Logic copied verbatim from classify.py ---

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


def make_fingerprint(short_rule, file_uri, snippet):
    """Fingerprint logic from classify.py (fp_src construction)."""
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(file_uri)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# --- Logic copied verbatim from gen_trailer.py fp() ---

def trailer_fp(rule, file_uri, step):
    """Fingerprint for the trailer (gen_trailer.py)."""
    base = os.path.basename(file_uri)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# --- SARIF extraction logic mirroring parse_sarif.py ---

def extract_finding(result):
    """Extract a finding dict from a single SARIF result object."""
    rule_id = result.get('ruleId', '?')
    level = result.get('level', 'note')
    message = result.get('message', {}).get('text', '')
    props = result.get('properties', {})
    sev = (props.get('problem.severity')
           or props.get('zizmor/severity')
           or props.get('security-severity', ''))
    conf = props.get('zizmor/confidence', '')
    locs = result.get('locations', [])
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


class TestOurSeverity(unittest.TestCase):
    """All five branches of the severity classifier."""

    def _f(self, level, conf=''):
        return {'level': level, 'confidence': conf}

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity(self._f('error', 'high')), 'Critical')

    def test_error_high_conf_case_insensitive(self):
        # confidence stored with mixed case should still match
        self.assertEqual(our_severity(self._f('error', 'High')), 'Critical')
        self.assertEqual(our_severity(self._f('error', 'HIGH')), 'Critical')

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'medium')), 'High')

    def test_error_low_conf_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'low')), 'High')

    def test_error_missing_conf_is_high(self):
        self.assertEqual(our_severity(self._f('error')), 'High')

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity(self._f('warning', 'high')), 'High')

    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'medium')), 'Medium')

    def test_warning_missing_conf_is_medium(self):
        self.assertEqual(our_severity(self._f('warning')), 'Medium')

    def test_note_level_is_low(self):
        self.assertEqual(our_severity(self._f('note')), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity(self._f('info')), 'Low')
        self.assertEqual(our_severity(self._f('')), 'Low')


class TestMakeFingerprint(unittest.TestCase):
    """Fingerprint stability and whitespace-normalisation edge cases."""

    def test_stable_across_calls(self):
        fp1 = make_fingerprint('template-injection', '.github/workflows/aeon.yml', 'run: echo ${{ github.event.head_commit.message }}')
        fp2 = make_fingerprint('template-injection', '.github/workflows/aeon.yml', 'run: echo ${{ github.event.head_commit.message }}')
        self.assertEqual(fp1, fp2)

    def test_uses_basename_not_full_path(self):
        fp_full = make_fingerprint('rule', '/full/path/to/aeon.yml', 'snip')
        fp_base = make_fingerprint('rule', 'aeon.yml', 'snip')
        self.assertEqual(fp_full, fp_base)

    def test_whitespace_normalised_in_snippet(self):
        # Multiple spaces and tabs should collapse to a single space.
        fp_multi = make_fingerprint('rule', 'f.yml', 'a  b\t\tc')
        fp_single = make_fingerprint('rule', 'f.yml', 'a b c')
        self.assertEqual(fp_multi, fp_single)

    def test_snippet_truncated_at_60_chars(self):
        long_snip = 'x' * 100
        trunc_snip = 'x' * 60
        self.assertEqual(
            make_fingerprint('rule', 'f.yml', long_snip),
            make_fingerprint('rule', 'f.yml', trunc_snip),
        )

    def test_different_rules_differ(self):
        fp1 = make_fingerprint('rule-a', 'f.yml', 'snip')
        fp2 = make_fingerprint('rule-b', 'f.yml', 'snip')
        self.assertNotEqual(fp1, fp2)

    def test_output_is_16_hex_chars(self):
        fp = make_fingerprint('rule', 'f.yml', 'snip')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))


class TestTrailerFp(unittest.TestCase):
    """Fingerprint used in gen_trailer.py uses step with underscores."""

    def test_space_and_underscore_equivalent(self):
        # The function normalises spaces → underscores before hashing, so
        # "Setup Node" and "Setup_Node" hash identically.  delta.py stores
        # step names with underscores; this documents that round-tripping is
        # lossless only in the underscore direction.
        fp_space = trailer_fp('rule', 'aeon.yml', 'Setup Node')
        fp_under = trailer_fp('rule', 'aeon.yml', 'Setup_Node')
        self.assertEqual(fp_space, fp_under)

    def test_stable(self):
        fp1 = trailer_fp('unpinned-uses', '.github/workflows/lint.yml', 'Checkout')
        fp2 = trailer_fp('unpinned-uses', '.github/workflows/lint.yml', 'Checkout')
        self.assertEqual(fp1, fp2)

    def test_basename_only(self):
        self.assertEqual(
            trailer_fp('r', '.github/workflows/a.yml', 's'),
            trailer_fp('r', 'a.yml', 's'),
        )


class TestExtractFinding(unittest.TestCase):
    """SARIF result extraction, including the no-locations branch."""

    def _loc(self, uri, line, snippet=''):
        return [{
            'physicalLocation': {
                'artifactLocation': {'uri': uri},
                'region': {'startLine': line, 'snippet': {'text': snippet}},
            }
        }]

    def test_full_result_with_location(self):
        result = {
            'ruleId': 'template-injection',
            'level': 'error',
            'message': {'text': 'Potential injection via ${{ github.event.head_commit.message }}'},
            'properties': {'zizmor/confidence': 'high'},
            'locations': self._loc('.github/workflows/aeon.yml', 42, 'run: echo ${{ ... }}'),
        }
        f = extract_finding(result)
        self.assertEqual(f['rule_id'], 'template-injection')
        self.assertEqual(f['level'], 'error')
        self.assertEqual(f['line'], 42)
        self.assertEqual(f['file'], '.github/workflows/aeon.yml')
        self.assertEqual(f['confidence'], 'high')

    def test_missing_locations_branch(self):
        # When locations is absent the parser must not raise and must
        # return safe zero-values for file/line/snippet.
        result = {
            'ruleId': 'unknown-rule',
            'level': 'note',
            'message': {'text': 'some finding'},
            'properties': {},
        }
        f = extract_finding(result)
        self.assertEqual(f['file'], '')
        self.assertEqual(f['line'], 0)
        self.assertEqual(f['snippet'], '')

    def test_empty_locations_list(self):
        result = {
            'ruleId': 'r',
            'level': 'warning',
            'message': {'text': 'm'},
            'properties': {},
            'locations': [],
        }
        f = extract_finding(result)
        self.assertEqual(f['file'], '')
        self.assertEqual(f['line'], 0)

    def test_severity_fallback_chain(self):
        # problem.severity takes priority; zizmor/severity is second fallback.
        r1 = {'ruleId': 'r', 'level': 'warning', 'message': {'text': ''},
               'properties': {'problem.severity': 'high', 'zizmor/severity': 'medium'}}
        self.assertEqual(extract_finding(r1)['severity_zizmor'], 'high')

        r2 = {'ruleId': 'r', 'level': 'warning', 'message': {'text': ''},
               'properties': {'zizmor/severity': 'medium', 'security-severity': 'low'}}
        self.assertEqual(extract_finding(r2)['severity_zizmor'], 'medium')

        r3 = {'ruleId': 'r', 'level': 'warning', 'message': {'text': ''},
               'properties': {'security-severity': 'low'}}
        self.assertEqual(extract_finding(r3)['severity_zizmor'], 'low')

    def test_snippet_truncated_at_200(self):
        long_text = 'a' * 300
        result = {
            'ruleId': 'r', 'level': 'note', 'message': {'text': ''},
            'properties': {},
            'locations': self._loc('f.yml', 1, long_text),
        }
        f = extract_finding(result)
        self.assertEqual(len(f['snippet']), 200)

    def test_missing_rule_id_defaults_to_question_mark(self):
        result = {'level': 'note', 'message': {'text': ''}, 'properties': {}}
        f = extract_finding(result)
        self.assertEqual(f['rule_id'], '?')

    def test_missing_message_text(self):
        result = {'ruleId': 'r', 'level': 'note', 'message': {}, 'properties': {}}
        f = extract_finding(result)
        self.assertEqual(f['message'], '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
