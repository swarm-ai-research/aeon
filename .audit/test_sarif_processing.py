"""
Unit tests for the SARIF-processing logic in classify.py / extract_steps.py / parse_sarif.py.

These scripts are not importable modules, so the pure functions are replicated
here from the source. Any change to the originals that breaks these tests
signals a logic regression in the severity mapping or location-extraction.

Run: python3 .audit/test_sarif_processing.py
"""

import hashlib
import re
import unittest


# --- Replicated from classify.py / extract_steps.py (must stay in sync) ----

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


def extract_finding(result, rules):
    """Core extraction logic from parse_sarif.py parse loop."""
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


# ---------------------------------------------------------------------------


class TestOurSeverity(unittest.TestCase):
    """Covers every branch of the four-way severity classifier."""

    def test_error_high_confidence_yields_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_confidence_yields_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_confidence_yields_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_missing_confidence_yields_high(self):
        # No 'confidence' key at all — must not raise KeyError
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_confidence_yields_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_confidence_yields_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_missing_confidence_yields_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_yields_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_yields_low(self):
        self.assertEqual(our_severity({'level': 'none', 'confidence': 'high'}), 'Low')

    def test_confidence_case_insensitive(self):
        # The production code calls .lower() on conf before comparing
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')


class TestExtractFinding(unittest.TestCase):
    """Covers location-extraction edge cases from parse_sarif.py."""

    def _result(self, **kwargs):
        base = {
            'ruleId': 'test-rule',
            'level': 'warning',
            'message': {'text': 'test message'},
            'properties': {'zizmor/confidence': 'high'},
            'locations': [],
        }
        base.update(kwargs)
        return base

    def test_empty_locations_produces_zero_defaults(self):
        f = extract_finding(self._result(locations=[]), rules={})
        self.assertEqual(f['file'], '')
        self.assertEqual(f['line'], 0)
        self.assertEqual(f['snippet'], '')

    def test_location_with_full_region(self):
        result = self._result(locations=[{
            'physicalLocation': {
                'artifactLocation': {'uri': '.github/workflows/ci.yml'},
                'region': {'startLine': 42, 'snippet': {'text': 'run: echo $VAR'}},
            }
        }])
        f = extract_finding(result, rules={})
        self.assertEqual(f['file'], '.github/workflows/ci.yml')
        self.assertEqual(f['line'], 42)
        self.assertEqual(f['snippet'], 'run: echo $VAR')

    def test_location_missing_region_startline(self):
        result = self._result(locations=[{
            'physicalLocation': {
                'artifactLocation': {'uri': 'ci.yml'},
                'region': {},
            }
        }])
        f = extract_finding(result, rules={})
        self.assertEqual(f['line'], 0)

    def test_missing_properties_uses_empty_strings(self):
        result = self._result()
        del result['properties']
        f = extract_finding(result, rules={})
        self.assertEqual(f['severity_zizmor'], '')
        self.assertEqual(f['confidence'], '')

    def test_severity_property_priority(self):
        # problem.severity takes priority over zizmor/severity
        result = self._result(properties={
            'problem.severity': 'high',
            'zizmor/severity': 'medium',
            'security-severity': 'low',
        })
        f = extract_finding(result, rules={})
        self.assertEqual(f['severity_zizmor'], 'high')

    def test_fallback_to_zizmor_severity(self):
        result = self._result(properties={
            'zizmor/severity': 'medium',
            'security-severity': 'low',
        })
        f = extract_finding(result, rules={})
        self.assertEqual(f['severity_zizmor'], 'medium')

    def test_snippet_truncated_at_200_chars(self):
        long_snippet = 'x' * 300
        result = self._result(locations=[{
            'physicalLocation': {
                'artifactLocation': {'uri': 'ci.yml'},
                'region': {'startLine': 1, 'snippet': {'text': long_snippet}},
            }
        }])
        f = extract_finding(result, rules={})
        self.assertEqual(len(f['snippet']), 200)

    def test_missing_ruleid_defaults_to_question_mark(self):
        result = self._result()
        del result['ruleId']
        f = extract_finding(result, rules={})
        self.assertEqual(f['rule_id'], '?')

    def test_missing_level_defaults_to_note(self):
        result = self._result()
        del result['level']
        f = extract_finding(result, rules={})
        self.assertEqual(f['level'], 'note')


if __name__ == '__main__':
    unittest.main()
