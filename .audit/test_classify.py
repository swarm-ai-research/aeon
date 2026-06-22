"""
Tests for classification and parsing logic mirrored from classify.py and parse_sarif.py.

Run: python3 .audit/test_classify.py

These test the pure logic functions whose module-level side effects (file I/O) would
otherwise make them hard to exercise: our_severity(), fingerprint generation, and
the SARIF location-extraction branch.
"""
import hashlib
import os
import re
import unittest


# ---------------------------------------------------------------------------
# Mirror of our_severity() from classify.py (lines 9-20)
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
# Mirror of fingerprint logic from classify.py (lines 27-30)
# ---------------------------------------------------------------------------

def make_fingerprint(f):
    short_rule = f['rule_id'].split('/')[-1]
    snip_key = re.sub(r'\s+', ' ', f.get('snippet', ''))[:60]
    file_short = os.path.basename(f['file'])
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Mirror of SARIF location extraction from parse_sarif.py (lines 18-28)
# ---------------------------------------------------------------------------

def extract_location(result):
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
    return uri, line, snippet


# ===========================================================================
# Tests
# ===========================================================================

class TestOurSeverity(unittest.TestCase):

    # Critical branch: error + high confidence
    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_conf_case_insensitive(self):
        # confidence is .lower()-ed before comparison
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    # High branch: error without high confidence
    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_missing_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    # High branch: warning + high confidence
    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_high_conf_case_insensitive(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')

    # Medium branch: warning without high confidence
    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_missing_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_warning_low_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    # Low branch: anything else (note, unknown, …)
    def test_note_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'unknown_level'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({'level': ''}), 'Low')


class TestFingerprint(unittest.TestCase):

    def test_fingerprint_is_16_hex_chars(self):
        f = {'rule_id': 'zizmor/artipacked', 'file': 'path/aeon.yml', 'snippet': 'uses: actions/checkout@v3'}
        fp = make_fingerprint(f)
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')

    def test_fingerprint_is_deterministic(self):
        f = {'rule_id': 'zizmor/artipacked', 'file': 'aeon.yml', 'snippet': 'uses: actions/checkout@v3'}
        self.assertEqual(make_fingerprint(f), make_fingerprint(f))

    def test_fingerprint_uses_basename_not_full_path(self):
        # Two findings differing only in leading path should get same fingerprint
        f1 = {'rule_id': 'rule', 'file': 'dir/file.yml', 'snippet': 'step'}
        f2 = {'rule_id': 'rule', 'file': 'other/dir/file.yml', 'snippet': 'step'}
        self.assertEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_fingerprint_normalises_internal_whitespace(self):
        # Multiple spaces in snippet are collapsed before hashing
        f1 = {'rule_id': 'rule', 'file': 'f.yml', 'snippet': 'a  b'}
        f2 = {'rule_id': 'rule', 'file': 'f.yml', 'snippet': 'a b'}
        self.assertEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_fingerprint_truncates_snippet_to_60(self):
        # Snippet beyond 60 chars does not affect the fingerprint
        base = 'x' * 60
        f1 = {'rule_id': 'rule', 'file': 'f.yml', 'snippet': base}
        f2 = {'rule_id': 'rule', 'file': 'f.yml', 'snippet': base + 'extra_stuff_ignored'}
        self.assertEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_fingerprint_differs_on_different_rule(self):
        f1 = {'rule_id': 'zizmor/rule-a', 'file': 'f.yml', 'snippet': 'x'}
        f2 = {'rule_id': 'zizmor/rule-b', 'file': 'f.yml', 'snippet': 'x'}
        self.assertNotEqual(make_fingerprint(f1), make_fingerprint(f2))

    def test_missing_snippet_does_not_crash(self):
        f = {'rule_id': 'rule', 'file': 'f.yml'}
        fp = make_fingerprint(f)
        self.assertEqual(len(fp), 16)


class TestExtractLocation(unittest.TestCase):

    # else-branch: no locations
    def test_empty_locations_list(self):
        uri, line, snippet = extract_location({'locations': []})
        self.assertEqual(uri, '')
        self.assertEqual(line, 0)
        self.assertEqual(snippet, '')

    def test_missing_locations_key(self):
        uri, line, snippet = extract_location({})
        self.assertEqual(uri, '')
        self.assertEqual(line, 0)
        self.assertEqual(snippet, '')

    # if-branch: full location present
    def test_full_location_extracted(self):
        result = {
            'locations': [{
                'physicalLocation': {
                    'artifactLocation': {'uri': '.github/workflows/aeon.yml'},
                    'region': {
                        'startLine': 42,
                        'snippet': {'text': 'run: echo ${{ github.event.pull_request.title }}'},
                    },
                }
            }]
        }
        uri, line, snippet = extract_location(result)
        self.assertEqual(uri, '.github/workflows/aeon.yml')
        self.assertEqual(line, 42)
        self.assertIn('echo', snippet)

    def test_missing_region_fields_default_to_zero_and_empty(self):
        result = {
            'locations': [{
                'physicalLocation': {
                    'artifactLocation': {'uri': 'workflow.yml'},
                    'region': {},
                }
            }]
        }
        uri, line, snippet = extract_location(result)
        self.assertEqual(uri, 'workflow.yml')
        self.assertEqual(line, 0)
        self.assertEqual(snippet, '')

    def test_only_first_location_is_used(self):
        result = {
            'locations': [
                {'physicalLocation': {
                    'artifactLocation': {'uri': 'first.yml'},
                    'region': {'startLine': 1, 'snippet': {'text': 'first'}},
                }},
                {'physicalLocation': {
                    'artifactLocation': {'uri': 'second.yml'},
                    'region': {'startLine': 2, 'snippet': {'text': 'second'}},
                }},
            ]
        }
        uri, line, snippet = extract_location(result)
        self.assertEqual(uri, 'first.yml')
        self.assertEqual(line, 1)
        self.assertEqual(snippet, 'first')

    def test_missing_snippet_in_region(self):
        result = {
            'locations': [{
                'physicalLocation': {
                    'artifactLocation': {'uri': 'w.yml'},
                    'region': {'startLine': 5},
                }
            }]
        }
        uri, line, snippet = extract_location(result)
        self.assertEqual(line, 5)
        self.assertEqual(snippet, '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
