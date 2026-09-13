#!/usr/bin/env python3
import json, hashlib, os, re
from collections import Counter

sarif = json.load(open('.audit/zizmor.sarif'))
results = sarif['runs'][0]['results']

def sev_from_zizmor(r):
    lvl = r.get('level', '?')
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

def loc(r):
    l = r['locations'][0]['physicalLocation']
    uri = l['artifactLocation']['uri']
    # Normalize: SARIF uri may be relative to the scan root. Prefix with .github/workflows/
    # when it doesn't already contain a directory component and the target lives there.
    if '/' not in uri and uri.endswith(('.yml', '.yaml')):
        uri = f".github/workflows/{uri}"
    return (
        uri,
        l['region'].get('startLine', 0),
        l['region'].get('endLine', 0),
    )

def fp(rule, fileuri, ctx):
    return hashlib.sha256(f"{rule}|{fileuri}|{ctx}".encode()).hexdigest()[:16]

findings = []
for r in results:
    rule = r.get('ruleId', '?')
    sev = sev_from_zizmor(r)
    fileuri, startLine, endLine = loc(r)
    ctx = f"L{startLine}"
    findings.append({
        'fingerprint': fp(rule, fileuri, ctx),
        'severity': sev,
        'rule_id': rule,
        'file': fileuri,
        'line': startLine,
        'end_line': endLine,
        'step': ctx,
        'msg': r['message']['text'][:200],
        'source': 'zizmor',
    })

alist = json.load(open('.audit/actionlint.json'))
def sev_from_actionlint(a):
    kind = a.get('kind', '')
    msg = a.get('message', '')
    if kind == 'expression':
        return 'High'
    if kind == 'shellcheck' and ('SC2086' in msg or 'SC2046' in msg) and 'github.' in msg:
        return 'High'
    return 'Medium'

for a in alist:
    rule = f"actionlint/{a.get('kind','?')}"
    kind_only = a.get('kind', '?')
    fileuri = a.get('filepath', '?')
    line = a.get('line', 0)
    ctx = f"L{line}"
    findings.append({
        'fingerprint': fp(kind_only, fileuri, ctx),
        'severity': sev_from_actionlint(a),
        'rule_id': rule,
        'file': fileuri,
        'line': line,
        'end_line': line,
        'step': ctx,
        'msg': a.get('message', '')[:200],
        'source': 'actionlint',
    })

handrolled = []
workflows = [
    '.github/workflows/messages.yml',
    '.github/workflows/aeon.yml',
    '.github/workflows/chain-runner.yml',
    '.github/workflows/fleet-runner.yml',
    '.github/workflows/gitlawb-repo-bootstrap.yml',
    '.github/workflows/sync-aeon-public-results.yml',
    '.github/workflows/sync-upstream.yml',
    '.github/workflows/lint.yml',
]
tojson_pat_single = re.compile(r"echo\s+'\$\{\{\s*toJson\(github\.event")
tojson_pat_double = re.compile(r'echo\s+"\$\{\{\s*toJson\(')
persist_pat = re.compile(r'persist-credentials:\s*true')
env_pat = re.compile(r'>>\s*"?\$\{?GITHUB_ENV\}?"?')
gh_event_pat = re.compile(r'\$\{\{\s*github\.event\.')

for f in workflows:
    if not os.path.exists(f):
        continue
    with open(f) as fh:
        content = fh.read()
    lines = content.split('\n')
    for i, ln in enumerate(lines, 1):
        if tojson_pat_single.search(ln) or tojson_pat_double.search(ln):
            handrolled.append(('toJson-into-shell', 'Critical', f, i, ln.strip()[:120]))
        if persist_pat.search(ln):
            window = '\n'.join(lines[i:i+15])
            if 'github.event.pull_request.head' in window:
                handrolled.append(('persist-credentials-poison', 'High', f, i, ln.strip()[:120]))
        if env_pat.search(ln):
            prev = '\n'.join(lines[max(0, i-4):i])
            if gh_event_pat.search(prev):
                handrolled.append(('github-env-injection', 'High', f, i, ln.strip()[:120]))

for rule, sev, fileuri, line, snippet in handrolled:
    ctx = f"L{line}"
    findings.append({
        'fingerprint': fp(f"handrolled/{rule}", fileuri, ctx),
        'severity': sev,
        'rule_id': f"handrolled/{rule}",
        'file': fileuri,
        'line': line,
        'end_line': line,
        'step': ctx,
        'msg': snippet,
        'source': 'hand-rolled',
    })

sev_counts = Counter(f['severity'] for f in findings)
print('total findings:', len(findings))
print('by severity:', dict(sev_counts))
print('by source:', Counter(f['source'] for f in findings))
print('handrolled findings:', len(handrolled))

with open('.audit/findings.json', 'w') as fh:
    json.dump(findings, fh, indent=2)
print('wrote .audit/findings.json')
