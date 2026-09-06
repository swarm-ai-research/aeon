#!/usr/bin/env python3
"""Build canonical findings from zizmor + actionlint outputs."""
import json
import hashlib
from collections import Counter

CONF_ORDER = {'unknown': 0, 'low': 1, 'medium': 2, 'high': 3}

def zizmor_severity(level, conf):
    conf_v = CONF_ORDER.get((conf or 'unknown').lower(), 0)
    if level == 'error' and conf_v >= CONF_ORDER['high']:
        return 'Critical'
    if level == 'error':
        return 'High'
    if level == 'warning' and conf_v >= CONF_ORDER['high']:
        return 'High'
    if level == 'warning':
        return 'Medium'
    return 'Low'

def actionlint_severity(msg, snippet):
    security_hits = ('SC2086', 'SC2046')
    if 'github.' in (snippet or '') or 'inputs.' in (snippet or ''):
        for h in security_hits:
            if h in msg:
                return 'High'
    return 'Medium'

def fp(rule_id, file, step_or_line):
    return hashlib.sha256(f"{rule_id}|{file}|{step_or_line}".encode()).hexdigest()[:16]

findings = []

# --- zizmor ---
data = json.load(open('.audit/zizmor.sarif'))
runs = data.get('runs', [])
if runs:
    for r in runs[0].get('results', []):
        rule = r.get('ruleId', '')
        level = r.get('level', '')
        msg = r.get('message', {}).get('text', '')
        props = r.get('properties', {}) or {}
        conf = props.get('problem.severity') or ''
        # zizmor puts confidence and severity in a props field
        for k, v in props.items():
            if 'confidence' in k.lower():
                conf = v
                break
        locs = r.get('locations', []) or []
        if not locs:
            continue
        pl = locs[0].get('physicalLocation', {})
        file_uri = pl.get('artifactLocation', {}).get('uri', '')
        # zizmor's SARIF uri is relative to the search prefix; prepend .github/workflows if missing
        if file_uri and not file_uri.startswith('.github/'):
            candidate = os.path.join('.github/workflows', file_uri)
            if os.path.exists(candidate):
                file_uri = candidate
        region = pl.get('region', {}) or {}
        line = region.get('startLine', 0)
        snippet = ''
        if 'snippet' in region:
            snippet = region['snippet'].get('text', '')
        # try to get step name from logicalLocations
        step = ''
        code_flows = r.get('codeFlows', []) or []
        for cf in code_flows:
            for tf in cf.get('threadFlows', []):
                for tflloc in tf.get('locations', []):
                    ll = tflloc.get('location', {}).get('logicalLocations', [])
                    for l in ll:
                        text = (l.get('message', {}) or {}).get('text', '')
                        if 'step' in text.lower():
                            step = text
                            break
        step_key = step or f"L{line}"
        severity = zizmor_severity(level, conf)
        findings.append({
            'fingerprint': fp(rule, file_uri, step_key),
            'severity': severity,
            'rule_id': rule,
            'file': file_uri,
            'line': line,
            'step': step,
            'message': msg,
            'snippet': (snippet or '')[:120],
            'source': 'zizmor',
            'confidence': conf,
            'level': level,
        })

# --- actionlint ---
al = json.load(open('.audit/actionlint.json'))
for d in al:
    msg = d.get('message', '')
    file = d.get('filepath', '')
    line = d.get('line', 0)
    snip = d.get('snippet', '')
    sev = actionlint_severity(msg, snip)
    findings.append({
        'fingerprint': fp(d.get('kind', 'actionlint'), file, f"L{line}"),
        'severity': sev,
        'rule_id': f"actionlint/{d.get('kind','')}",
        'file': file,
        'line': line,
        'step': '',
        'message': msg[:200],
        'snippet': (snip or '')[:120],
        'source': 'actionlint',
        'confidence': '',
        'level': '',
    })

# --- hand-rolled ---
# Load workflow files
import os, re
handrolled = []

wf_files = []
for base in ['.github/workflows', '.github/actions']:
    if os.path.isdir(base):
        for root, dirs, files in os.walk(base):
            for f in files:
                if f.endswith(('.yml', '.yaml')):
                    wf_files.append(os.path.join(root, f))

for wf in wf_files:
    text = open(wf).read()
    lines = text.split('\n')
    # 1) toJson-into-shell injection: echo '${{ toJson(...) }}' | jq or $(echo '${{ toJson(...) }}')
    for i, ln in enumerate(lines, 1):
        if re.search(r"echo\s+['\"]?\$\{\{\s*toJson\(", ln):
            handrolled.append({
                'fingerprint': fp('handrolled/tojson-shell-injection', wf, f"L{i}"),
                'severity': 'Critical',
                'rule_id': 'handrolled/tojson-shell-injection',
                'file': wf,
                'line': i,
                'step': '',
                'message': 'toJson(github.*) interpolated into shell via echo — attacker-controlled JSON breaks single quotes',
                'snippet': ln.strip()[:120],
                'source': 'hand-rolled',
                'confidence': '',
                'level': '',
            })
        # 2) GITHUB_ENV / GITHUB_OUTPUT writes with user data
        m = re.search(r'>>\s*"?\$\{?GITHUB_(ENV|OUTPUT)', ln)
        if m and '${{' in ln and ('github.event' in ln or 'inputs.' in ln or 'client_payload' in ln):
            handrolled.append({
                'fingerprint': fp('handrolled/github-env-write-user-data', wf, f"L{i}"),
                'severity': 'High',
                'rule_id': 'handrolled/github-env-write-user-data',
                'file': wf,
                'line': i,
                'step': '',
                'message': 'Writing user-controlled data to GITHUB_ENV/GITHUB_OUTPUT — newline injection bypasses masking',
                'snippet': ln.strip()[:120],
                'source': 'hand-rolled',
                'confidence': '',
                'level': '',
            })
    # 3) persist-credentials + PR head ref check
    # Look for actions/checkout without persist-credentials: false followed by PR ref
    txt = text
    if 'actions/checkout' in txt and 'pull_request_target' in txt:
        if 'persist-credentials: false' not in txt and 'pull_request.head.sha' in txt:
            handrolled.append({
                'fingerprint': fp('handrolled/persist-credentials-prtarget', wf, 'file'),
                'severity': 'Critical',
                'rule_id': 'handrolled/persist-credentials-prtarget',
                'file': wf,
                'line': 0,
                'step': '',
                'message': 'checkout without persist-credentials: false in a pull_request_target workflow using head.sha — poisoned pipeline',
                'snippet': '',
                'source': 'hand-rolled',
                'confidence': '',
                'level': '',
            })
    # 4) Fleet-specific: gh workflow run / gh api dispatches with ${{ inputs.* }} directly in run:
    for i, ln in enumerate(lines, 1):
        if re.search(r'gh\s+(workflow\s+run|api\s+repos.*/dispatches)', ln) and '${{' in ln and ('inputs.' in ln or 'github.event' in ln):
            handrolled.append({
                'fingerprint': fp('handrolled/gh-dispatch-user-data', wf, f"L{i}"),
                'severity': 'High',
                'rule_id': 'handrolled/gh-dispatch-user-data',
                'file': wf,
                'line': i,
                'step': '',
                'message': 'gh workflow-run/api dispatch passing user-controlled ${{ ... }} without env intermediary',
                'snippet': ln.strip()[:120],
                'source': 'hand-rolled',
                'confidence': '',
                'level': '',
            })

findings.extend(handrolled)

open('.audit/findings.json', 'w').write(json.dumps(findings, indent=2))

# Print summary
print(f'total findings: {len(findings)}')
print()
by_sev = Counter(f['severity'] for f in findings)
print('by severity:', dict(by_sev))
print()
by_source = Counter(f['source'] for f in findings)
print('by source:', dict(by_source))
print()
by_rule = Counter(f['rule_id'] for f in findings)
print('by rule:')
for rule, cnt in by_rule.most_common():
    print(f'  {cnt:4d} {rule}')
print()
print('=== CRITICAL ===')
for f in findings:
    if f['severity'] == 'Critical':
        print(f"  {f['file']}:{f['line']} [{f['rule_id']}] {f['message'][:80]}")
print()
print('=== HIGH ===')
for f in findings:
    if f['severity'] == 'High':
        print(f"  {f['file']}:{f['line']} [{f['rule_id']}] {f['message'][:80]}")
