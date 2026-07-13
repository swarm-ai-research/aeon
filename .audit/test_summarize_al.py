"""
Tests for the core logic in summarize_al.py and parse_sarif.py.

These scripts are not importable (they execute on load), so the testable
functions are inlined here as verbatim copies.  Any divergence between
the copies and the originals is itself a test signal.

Run: python .audit/test_summarize_al.py
"""
import sys
from collections import Counter

# ── Logic from summarize_al.py ────────────────────────────────────────────────

TRACKED_CODES = ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']


def categorize(findings):
    codes = Counter()
    for f in findings:
        msg = f.get('message', '')
        matched = False
        for code in TRACKED_CODES:
            if code in msg:
                codes[code] += 1
                matched = True
                break
        if not matched:
            codes['other'] += 1
    return dict(codes)


def high_candidates(findings):
    return [
        f for f in findings
        if ('SC2086' in f.get('message', '') or 'SC2046' in f.get('message', ''))
        and 'github.' in f.get('message', '').lower()
    ]


# ── Logic from parse_sarif.py ─────────────────────────────────────────────────

def parse_runs(data):
    all_findings = []
    for run in data.get('runs', []):
        for r in run.get('results', []):
            rule_id = r.get('ruleId', '?')
            level = r.get('level', 'note')
            message = r.get('message', {}).get('text', '')
            props = r.get('properties', {})
            sev = (props.get('problem.severity')
                   or props.get('zizmor/severity')
                   or props.get('security-severity', ''))
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
                'rule_id': rule_id, 'level': level,
                'severity_zizmor': sev, 'confidence': conf,
                'message': message, 'file': uri,
                'line': line, 'snippet': snippet[:200],
            })
    return all_findings


# ── Test harness ──────────────────────────────────────────────────────────────

passed = failed = 0


def ok(cond, label):
    global passed, failed
    if cond:
        passed += 1
        print(f'  ok  {label}')
    else:
        failed += 1
        print(f'  FAIL {label}', file=sys.stderr)


# ── categorize() ─────────────────────────────────────────────────────────────

print('categorize:')
ok(categorize([]) == {}, 'empty list -> empty counts')
ok(categorize([{'message': 'no known code here'}]) == {'other': 1},
   'unrecognised code -> other')
ok(categorize([{}]) == {'other': 1},
   'missing message key -> other')
ok(categorize([{'message': 'SC2086 unquoted'}]) == {'SC2086': 1},
   'SC2086 counted')
ok(categorize([{'message': 'SC2046 unquoted'}]) == {'SC2046': 1},
   'SC2046 counted')
# SC2086 precedes SC2046 in TRACKED_CODES; the loop breaks on first match.
ok(categorize([{'message': 'SC2086 and SC2046 both present'}]) == {'SC2086': 1},
   'SC2086 wins over SC2046 when both appear (first-match breaks)')
ok(categorize([{'message': 'SC2155 expand'}, {'message': 'SC2155 expand'}]) == {'SC2155': 2},
   'same code counted across multiple findings')

# ── high_candidates() ────────────────────────────────────────────────────────

print('\nhigh_candidates:')
ok(high_candidates([]) == [],
   'empty list -> no candidates')
ok(len(high_candidates([{'message': 'SC2086 in github.event.inputs.name'}])) == 1,
   'SC2086 + github. -> high candidate')
ok(len(high_candidates([{'message': 'SC2046 references $GITHUB.SHA'}])) == 1,
   'SC2046 + GITHUB. (case-insensitive match) -> high candidate')
ok(high_candidates([{'message': 'SC2086 unquoted plain var'}]) == [],
   'SC2086 without github. -> not a candidate')
ok(high_candidates([{'message': 'references github.event.name'}]) == [],
   'github. without SC2086/SC2046 -> not a candidate')
ok(high_candidates([{'message': 'SC2153 github.context'}]) == [],
   'SC2153 + github. does NOT trigger (only SC2086/SC2046 are checked)')
ok(high_candidates([{'message': 'SC2129 github.actor'}]) == [],
   'SC2129 + github. does NOT trigger')

# ── parse_runs() ─────────────────────────────────────────────────────────────

print('\nparse_runs:')
ok(parse_runs({}) == [],
   'missing runs key -> empty findings')
ok(parse_runs({'runs': []}) == [],
   'empty runs list -> empty findings')
ok(parse_runs({'runs': [{'results': []}]}) == [],
   'empty results list -> empty findings')

# else-branch: result with no locations
no_loc = parse_runs({'runs': [{'results': [
    {'ruleId': 'test-rule', 'level': 'error', 'message': {'text': 'msg'}}
]}]})
ok(len(no_loc) == 1, 'result without locations key still parsed')
ok(no_loc[0]['file'] == '', 'no locations -> file defaults to empty string')
ok(no_loc[0]['line'] == 0, 'no locations -> line defaults to 0')
ok(no_loc[0]['snippet'] == '', 'no locations -> snippet defaults to empty string')

# else-branch: explicit empty locations list
empty_locs = parse_runs({'runs': [{'results': [
    {'ruleId': 'r', 'locations': []}
]}]})
ok(empty_locs[0]['file'] == '', 'empty locations list -> else branch taken')

# severity fallback chain: problem.severity -> zizmor/severity -> security-severity -> ''


def _sev(props):
    return parse_runs({'runs': [{'results': [{'ruleId': 'r', 'properties': props}]}]})[0]['severity_zizmor']


ok(_sev({'problem.severity': 'high'}) == 'high',
   'problem.severity used first')
ok(_sev({'zizmor/severity': 'medium'}) == 'medium',
   'zizmor/severity used when problem.severity absent')
ok(_sev({'security-severity': 'low'}) == 'low',
   'security-severity used as last resort')
ok(_sev({}) == '',
   'no severity properties -> empty string')

# only the first location is used
multi_loc = parse_runs({'runs': [{'results': [{'ruleId': 'r', 'locations': [
    {'physicalLocation': {'artifactLocation': {'uri': 'first.yml'},
                         'region': {'startLine': 5}}},
    {'physicalLocation': {'artifactLocation': {'uri': 'second.yml'},
                         'region': {'startLine': 99}}},
]}]}]})[0]
ok(multi_loc['file'] == 'first.yml', 'only first location used for file uri')
ok(multi_loc['line'] == 5, 'only first location used for line number')

# snippet truncated at 200 chars
long_snip = parse_runs({'runs': [{'results': [{'ruleId': 'r', 'locations': [
    {'physicalLocation': {'artifactLocation': {'uri': 'f.yml'},
                         'region': {'startLine': 1,
                                    'snippet': {'text': 'x' * 300}}}}
]}]}]})[0]
ok(len(long_snip['snippet']) == 200, 'snippet truncated to 200 characters')

# default level when level key absent
no_level = parse_runs({'runs': [{'results': [{'ruleId': 'r'}]}]})[0]
ok(no_level['level'] == 'note', 'absent level defaults to "note"')

# ── Results ──────────────────────────────────────────────────────────────────

print(f'\n{passed} passed, {failed} failed')
if failed:
    sys.exit(1)
