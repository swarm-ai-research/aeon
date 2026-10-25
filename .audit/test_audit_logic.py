"""
Unit tests for audit analysis helper logic.

The production scripts in this directory (classify.py, delta.py, parse_sarif.py)
are not importable as modules (top-level side-effects), so the pure functions are
replicated here verbatim to enable isolated testing. Any drift between these copies
and the originals is itself a signal that the originals need refactoring.

Run: python -m pytest .audit/test_audit_logic.py  (or python .audit/test_audit_logic.py)
"""

import hashlib
import os
import unittest


# ---------------------------------------------------------------------------
# Replicated from classify.py — our_severity()
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
# Replicated from delta.py — fp_for()
# ---------------------------------------------------------------------------

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Replicated from parse_sarif.py — extract_findings()
# ---------------------------------------------------------------------------

def extract_findings(data):
    """Parse a SARIF data dict into a flat list of finding dicts."""
    runs = data.get('runs', [])
    all_findings = []
    for run in runs:
        for r in run.get('results', []):
            rule_id = r.get('ruleId', '?')
            level = r.get('level', 'note')
            message = r.get('message', {}).get('text', '')
            props = r.get('properties', {})
            sev = (
                props.get('problem.severity')
                or props.get('zizmor/severity')
                or props.get('security-severity', '')
            )
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
            all_findings.append({
                'rule_id': rule_id,
                'level': level,
                'severity_zizmor': sev,
                'confidence': conf,
                'message': message,
                'file': uri,
                'line': line,
                'snippet': snippet[:200],
            })
    return all_findings


# ===========================================================================
# Tests
# ===========================================================================

class TestOurSeverity(unittest.TestCase):
    """Tests for the severity classification function used by classify.py."""

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_missing_confidence_is_high(self):
        # .get('confidence', '') returns '' when key absent → not 'high' → High
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_is_low_regardless_of_confidence(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'info'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({'level': ''}), 'Low')

    def test_confidence_comparison_is_case_insensitive(self):
        # classify.py does .lower() — 'HIGH' must behave the same as 'high'
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')

    def test_confidence_mixed_case(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')


class TestFpFor(unittest.TestCase):
    """Tests for the fingerprint function used by delta.py."""

    def test_output_is_16_hex_chars(self):
        fp = fp_for('unpinned-uses', '.github/workflows/ci.yml', 'Setup Node')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_basename_is_used_not_full_path(self):
        fp1 = fp_for('rule', '.github/workflows/foo.yml', 'step')
        fp2 = fp_for('rule', 'foo.yml', 'step')
        self.assertEqual(fp1, fp2)

    def test_different_directories_same_filename_match(self):
        fp1 = fp_for('rule', 'a/b/c/foo.yml', 'step')
        fp2 = fp_for('rule', 'x/y/foo.yml', 'step')
        self.assertEqual(fp1, fp2)

    def test_underscore_and_space_in_step_yield_different_fps(self):
        # delta.py tries both variants because prior audit stored underscored names.
        # The two must be distinct for the dual-lookup to have any meaning.
        fp_space = fp_for('rule', 'foo.yml', 'Setup Node')
        fp_under = fp_for('rule', 'foo.yml', 'Setup_Node')
        self.assertNotEqual(fp_space, fp_under)

    def test_deterministic_across_calls(self):
        fp1 = fp_for('unpinned-uses', 'foo.yml', 'step')
        fp2 = fp_for('unpinned-uses', 'foo.yml', 'step')
        self.assertEqual(fp1, fp2)

    def test_different_rules_yield_different_fps(self):
        fp1 = fp_for('rule-a', 'foo.yml', 'step')
        fp2 = fp_for('rule-b', 'foo.yml', 'step')
        self.assertNotEqual(fp1, fp2)

    def test_empty_fields_do_not_crash(self):
        fp = fp_for('', '', '')
        self.assertEqual(len(fp), 16)


class TestExtractFindings(unittest.TestCase):
    """Tests for SARIF parsing logic used by parse_sarif.py (processes zizmor output)."""

    def test_empty_dict_returns_no_findings(self):
        self.assertEqual(extract_findings({}), [])

    def test_empty_runs_list_returns_no_findings(self):
        self.assertEqual(extract_findings({'runs': []}), [])

    def test_run_with_empty_results_returns_no_findings(self):
        self.assertEqual(extract_findings({'runs': [{'results': []}]}), [])

    def test_result_with_no_locations_key_yields_blank_location(self):
        sarif = {'runs': [{'results': [
            {'ruleId': 'r', 'level': 'warning', 'message': {'text': 'msg'}},
        ]}]}
        findings = extract_findings(sarif)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['file'], '')
        self.assertEqual(findings[0]['line'], 0)
        self.assertEqual(findings[0]['snippet'], '')

    def test_result_with_empty_locations_list_yields_blank_location(self):
        sarif = {'runs': [{'results': [
            {'ruleId': 'r', 'level': 'warning', 'message': {'text': ''}, 'locations': []},
        ]}]}
        findings = extract_findings(sarif)
        self.assertEqual(findings[0]['file'], '')
        self.assertEqual(findings[0]['line'], 0)

    def test_result_with_multiple_locations_uses_first_only(self):
        sarif = {'runs': [{'results': [
            {
                'ruleId': 'r', 'level': 'note', 'message': {},
                'locations': [
                    {'physicalLocation': {
                        'artifactLocation': {'uri': 'first.yml'},
                        'region': {'startLine': 10},
                    }},
                    {'physicalLocation': {
                        'artifactLocation': {'uri': 'second.yml'},
                        'region': {'startLine': 20},
                    }},
                ],
            }
        ]}]}
        findings = extract_findings(sarif)
        self.assertEqual(findings[0]['file'], 'first.yml')
        self.assertEqual(findings[0]['line'], 10)

    def test_severity_property_resolution_order(self):
        # problem.severity > zizmor/severity > security-severity
        sarif = {'runs': [{'results': [
            {
                'ruleId': 'r', 'level': 'note', 'message': {},
                'properties': {
                    'problem.severity': 'high',
                    'zizmor/severity': 'medium',
                    'security-severity': 'low',
                },
                'locations': [],
            }
        ]}]}
        self.assertEqual(extract_findings(sarif)[0]['severity_zizmor'], 'high')

    def test_severity_falls_back_to_zizmor_severity(self):
        sarif = {'runs': [{'results': [
            {
                'ruleId': 'r', 'level': 'note', 'message': {},
                'properties': {'zizmor/severity': 'medium', 'security-severity': 'low'},
                'locations': [],
            }
        ]}]}
        self.assertEqual(extract_findings(sarif)[0]['severity_zizmor'], 'medium')

    def test_severity_falls_back_to_security_severity(self):
        sarif = {'runs': [{'results': [
            {
                'ruleId': 'r', 'level': 'note', 'message': {},
                'properties': {'security-severity': 'low'},
                'locations': [],
            }
        ]}]}
        self.assertEqual(extract_findings(sarif)[0]['severity_zizmor'], 'low')

    def test_snippet_truncated_at_200_chars(self):
        long_snip = 'x' * 500
        sarif = {'runs': [{'results': [
            {
                'ruleId': 'r', 'level': 'note', 'message': {},
                'locations': [{'physicalLocation': {
                    'artifactLocation': {'uri': 'f.yml'},
                    'region': {'startLine': 1, 'snippet': {'text': long_snip}},
                }}],
            }
        ]}]}
        findings = extract_findings(sarif)
        self.assertEqual(len(findings[0]['snippet']), 200)

    def test_missing_rule_id_defaults_to_question_mark(self):
        sarif = {'runs': [{'results': [
            {'level': 'note', 'message': {'text': ''}, 'locations': []},
        ]}]}
        self.assertEqual(extract_findings(sarif)[0]['rule_id'], '?')

    def test_missing_level_defaults_to_note(self):
        sarif = {'runs': [{'results': [
            {'ruleId': 'r', 'message': {'text': ''}, 'locations': []},
        ]}]}
        self.assertEqual(extract_findings(sarif)[0]['level'], 'note')

    def test_multiple_runs_aggregated(self):
        sarif = {'runs': [
            {'results': [{'ruleId': 'r1', 'level': 'error', 'message': {}, 'locations': []}]},
            {'results': [{'ruleId': 'r2', 'level': 'warning', 'message': {}, 'locations': []}]},
        ]}
        findings = extract_findings(sarif)
        self.assertEqual(len(findings), 2)
        rule_ids = {f['rule_id'] for f in findings}
        self.assertEqual(rule_ids, {'r1', 'r2'})


# ---------------------------------------------------------------------------
# Replicated from normalize.py — extract_step_name(), normalize_file(),
# sev_zizmor(), sev_actionlint()
# ---------------------------------------------------------------------------

import re as _re

_STEP_NAME_RE = _re.compile(r'^\s*(?:-\s+)?name:\s*(.+?)\s*$', _re.MULTILINE)


def extract_step_name(snippet: str):
    if not snippet:
        return None
    m = _STEP_NAME_RE.search(snippet)
    if m:
        return m.group(1).strip().strip('"\'')
    return None


def normalize_file(uri):
    if uri and '/' not in uri and uri.endswith(('.yml', '.yaml')):
        return f'.github/workflows/{uri}'
    return uri


def sev_zizmor_normalize(r):
    """normalize.py version — case-sensitive 'High' (no .lower())."""
    lvl = r.get('level')
    conf = r.get('properties', {}).get('zizmor/confidence', '')
    if lvl == 'error' and conf == 'High':
        return 'Critical'
    if lvl == 'error':
        return 'High'
    if lvl == 'warning' and conf == 'High':
        return 'High'
    if lvl == 'warning':
        return 'Medium'
    return 'Low'


def sev_actionlint(a):
    kind = a.get('kind', '')
    msg = a.get('message', '')
    if kind == 'expression':
        return 'High'
    if kind == 'shellcheck' and ('SC2086' in msg or 'SC2046' in msg) and 'github.' in msg:
        return 'High'
    return 'Medium'


# ===========================================================================
# Tests for normalize.py helpers
# ===========================================================================

class TestExtractStepName(unittest.TestCase):
    """Tests for normalize.py extract_step_name()."""

    def test_empty_string_returns_none(self):
        self.assertIsNone(extract_step_name(''))

    def test_none_like_falsy_returns_none(self):
        # snippet=None is not passed by the caller but the guard handles any falsy value
        self.assertIsNone(extract_step_name(None))

    def test_snippet_with_name_returns_it(self):
        snippet = '      - name: Setup Node\n        uses: actions/setup-node@v3'
        self.assertEqual(extract_step_name(snippet), 'Setup Node')

    def test_snippet_without_name_key_returns_none(self):
        snippet = '      uses: actions/checkout@v4\n      with:\n        fetch-depth: 0'
        self.assertIsNone(extract_step_name(snippet))

    def test_quoted_name_strips_quotes(self):
        snippet = "      - name: 'Run Tests'\n"
        self.assertEqual(extract_step_name(snippet), 'Run Tests')

    def test_double_quoted_name_strips_quotes(self):
        snippet = '      - name: "Deploy"\n'
        self.assertEqual(extract_step_name(snippet), 'Deploy')

    def test_name_with_leading_whitespace_trimmed(self):
        snippet = 'name:   Checkout Code  \n'
        self.assertEqual(extract_step_name(snippet), 'Checkout Code')

    def test_multiline_snippet_uses_first_name(self):
        snippet = 'name: First Step\nname: Second Step\n'
        self.assertEqual(extract_step_name(snippet), 'First Step')


class TestNormalizeFile(unittest.TestCase):
    """Tests for normalize.py normalize_file()."""

    def test_bare_yml_filename_gets_workflow_prefix(self):
        self.assertEqual(normalize_file('ci.yml'), '.github/workflows/ci.yml')

    def test_bare_yaml_filename_gets_workflow_prefix(self):
        self.assertEqual(normalize_file('release.yaml'), '.github/workflows/release.yaml')

    def test_path_with_slash_is_unchanged(self):
        self.assertEqual(normalize_file('.github/workflows/ci.yml'), '.github/workflows/ci.yml')

    def test_empty_string_is_unchanged(self):
        self.assertEqual(normalize_file(''), '')

    def test_none_is_unchanged(self):
        self.assertIsNone(normalize_file(None))

    def test_non_yaml_extension_is_unchanged(self):
        self.assertEqual(normalize_file('ci.json'), 'ci.json')

    def test_filename_with_path_but_yaml_ext_unchanged(self):
        self.assertEqual(normalize_file('subdir/ci.yml'), 'subdir/ci.yml')


class TestSevZizmor(unittest.TestCase):
    """Tests for normalize.py sev_zizmor() — note the case-SENSITIVE 'High' check."""

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(sev_zizmor_normalize({'level': 'error', 'properties': {'zizmor/confidence': 'High'}}), 'Critical')

    def test_error_lowercase_high_is_NOT_critical(self):
        # normalize.py does NOT call .lower() — 'high' != 'High' → falls to plain error branch
        self.assertEqual(sev_zizmor_normalize({'level': 'error', 'properties': {'zizmor/confidence': 'high'}}), 'High')

    def test_error_no_confidence_is_high(self):
        self.assertEqual(sev_zizmor_normalize({'level': 'error', 'properties': {}}), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(sev_zizmor_normalize({'level': 'warning', 'properties': {'zizmor/confidence': 'High'}}), 'High')

    def test_warning_lowercase_high_is_medium(self):
        self.assertEqual(sev_zizmor_normalize({'level': 'warning', 'properties': {'zizmor/confidence': 'high'}}), 'Medium')

    def test_warning_no_confidence_is_medium(self):
        self.assertEqual(sev_zizmor_normalize({'level': 'warning', 'properties': {}}), 'Medium')

    def test_note_level_is_low(self):
        self.assertEqual(sev_zizmor_normalize({'level': 'note', 'properties': {'zizmor/confidence': 'High'}}), 'Low')

    def test_missing_properties_key_is_low_for_note(self):
        self.assertEqual(sev_zizmor_normalize({'level': 'note'}), 'Low')


class TestSevActionlint(unittest.TestCase):
    """Tests for normalize.py sev_actionlint()."""

    def test_expression_kind_is_high(self):
        self.assertEqual(sev_actionlint({'kind': 'expression', 'message': 'some expr issue'}), 'High')

    def test_shellcheck_sc2086_with_github_ref_is_high(self):
        msg = 'SC2086: Double quote to prevent globbing (github.event.inputs.foo)'
        self.assertEqual(sev_actionlint({'kind': 'shellcheck', 'message': msg}), 'High')

    def test_shellcheck_sc2046_with_github_ref_is_high(self):
        msg = 'SC2046: Quote this to prevent word splitting. (github.sha)'
        self.assertEqual(sev_actionlint({'kind': 'shellcheck', 'message': msg}), 'High')

    def test_shellcheck_sc2086_without_github_ref_is_medium(self):
        msg = 'SC2086: Double quote to prevent globbing (MY_VAR)'
        self.assertEqual(sev_actionlint({'kind': 'shellcheck', 'message': msg}), 'Medium')

    def test_shellcheck_other_code_is_medium(self):
        msg = 'SC2034: foo appears unused'
        self.assertEqual(sev_actionlint({'kind': 'shellcheck', 'message': msg}), 'Medium')

    def test_unknown_kind_is_medium(self):
        self.assertEqual(sev_actionlint({'kind': 'syntax', 'message': 'unexpected token'}), 'Medium')

    def test_missing_kind_is_medium(self):
        self.assertEqual(sev_actionlint({'message': 'some error'}), 'Medium')

    def test_expression_kind_ignores_message_content(self):
        # kind='expression' → High regardless of message
        self.assertEqual(sev_actionlint({'kind': 'expression', 'message': ''}), 'High')


if __name__ == '__main__':
    unittest.main()
