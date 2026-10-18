"""Build canonical findings from zizmor + actionlint + hand-rolled checks.

Matches the fingerprint convention from the prior 2026-09-27 audit so delta
classification stays stable.
"""
import json, os, hashlib, re, glob, pathlib
from collections import Counter

os.chdir('/home/runner/work/aeon/aeon')

STEP_NAME_RE = re.compile(r'^\s*(?:-\s+)?name:\s*(.+?)\s*$', re.MULTILINE)

def extract_step_name(snippet: str):
    if not snippet:
        return None
    m = STEP_NAME_RE.search(snippet)
    if m:
        return m.group(1).strip().strip('"\'')
    return None

def normalize_file(uri):
    if uri and '/' not in uri and uri.endswith(('.yml', '.yaml')):
        return f'.github/workflows/{uri}'
    return uri

def fp(rule, fileuri, ctx):
    return hashlib.sha256(f'{rule}|{fileuri}|{ctx}'.encode()).hexdigest()[:16]

def sev_zizmor(r):
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

findings = []

sarif = json.load(open('.audit/zizmor.sarif'))
for r in sarif['runs'][0]['results']:
    rule = r.get('ruleId', '?')
    sev = sev_zizmor(r)
    loc = r['locations'][0]['physicalLocation']
    fileuri = normalize_file(loc['artifactLocation']['uri'])
    region = loc.get('region', {})
    start_line = region.get('startLine', 0)
    end_line = region.get('endLine', start_line)
    snippet_text = region.get('snippet', {}).get('text', '')
    step_name = extract_step_name(snippet_text)
    ctx = step_name if step_name else f'L{start_line}'
    findings.append({
        'fingerprint': fp(rule, fileuri, ctx),
        'severity': sev,
        'rule_id': rule,
        'file': fileuri,
        'line': start_line,
        'end_line': end_line,
        'step': ctx,
        'step_name': step_name,
        'confidence': r.get('properties', {}).get('zizmor/confidence'),
        'msg': r['message']['text'],
        'snippet': snippet_text[:400],
        'source': 'zizmor',
    })

def sev_actionlint(a):
    kind = a.get('kind', '')
    msg = a.get('message', '')
    if kind == 'expression':
        return 'High'
    if kind == 'shellcheck' and ('SC2086' in msg or 'SC2046' in msg) and 'github.' in msg:
        return 'High'
    return 'Medium'

alist = json.load(open('.audit/actionlint.json'))
for a in alist:
    kind = a.get('kind', '?')
    rule_full = f'actionlint/{kind}'
    fileuri = a.get('filepath', '?')
    line = a.get('line', 0)
    sc = ''
    m = re.search(r'(SC\d+)', a.get('message', ''))
    if m: sc = m.group(1)
    ctx = f'{sc}:L{line}' if sc else f'L{line}'
    findings.append({
        'fingerprint': fp(kind, fileuri, ctx),
        'severity': sev_actionlint(a),
        'rule_id': f'{rule_full}/{sc}' if sc else rule_full,
        'file': fileuri, 'line': line, 'end_line': line,
        'step': ctx, 'step_name': None,
        'msg': a.get('message', ''),
        'snippet': a.get('snippet', '')[:400],
        'source': 'actionlint',
    })

# Hand-rolled
workflows = sorted(glob.glob('.github/workflows/*.yml') + glob.glob('.github/workflows/*.yaml'))
tojson_shell_pat = re.compile(r"(?:echo|printf)\s+[\"']?\$\{\{\s*toJson\(")
persist_pat = re.compile(r'persist-credentials:\s*true')
env_pat = re.compile(r'>>\s*"?\$\{?GITHUB_(?:ENV|OUTPUT)\}?"?')
gh_event_direct_pat = re.compile(r'\$\{\{\s*github\.event\.[^}]+\}\}')
uses_ref_pat = re.compile(
    r'^\s*(?:-\s+)?uses:\s+([A-Za-z0-9._-]+)/([A-Za-z0-9._/-]+)@([A-Za-z0-9._-]+)', re.MULTILINE)
TRUSTED = {'actions', 'github', 'docker', 'aws-actions'}

handrolled = []
for f in workflows:
    text = pathlib.Path(f).read_text()
    lines = text.split('\n')
    for i, ln in enumerate(lines, 1):
        if tojson_shell_pat.search(ln):
            handrolled.append(('handrolled/tojson-shell', 'Critical', f, i, ln.strip()[:200]))
        if persist_pat.search(ln):
            window = '\n'.join(lines[i:i+20])
            if 'github.event.pull_request.head' in window:
                handrolled.append(('handrolled/persist-credentials-poison', 'High', f, i, ln.strip()[:200]))
        if env_pat.search(ln):
            prev = '\n'.join(lines[max(0, i-4):i])
            if gh_event_direct_pat.search(prev):
                handrolled.append(('handrolled/github-env-injection', 'High', f, i, ln.strip()[:200]))
    for m in uses_ref_pat.finditer(text):
        owner, name, ref = m.group(1), m.group(2), m.group(3)
        if owner in TRUSTED:
            continue
        if not re.fullmatch(r'[0-9a-f]{40}', ref):
            line = text[:m.start()].count('\n') + 1
            handrolled.append(('handrolled/mutable-third-party-ref', 'Medium', f, line,
                               f'uses: {owner}/{name}@{ref}'[:200]))

for rule, sev, fileuri, line, snippet in handrolled:
    ctx = f'L{line}'
    findings.append({
        'fingerprint': fp(rule, fileuri, ctx),
        'severity': sev, 'rule_id': rule, 'file': fileuri,
        'line': line, 'end_line': line, 'step': ctx, 'step_name': None,
        'msg': snippet, 'snippet': snippet, 'source': 'hand-rolled',
    })

sev_counts = Counter(f['severity'] for f in findings)
src_counts = Counter(f['source'] for f in findings)
print('TOTAL:', len(findings))
print('By severity:', dict(sev_counts))
print('By source:', dict(src_counts))
print('hand-rolled:', len(handrolled))

with open('.audit/findings.json', 'w') as fh:
    json.dump(findings, fh, indent=1)
print('Wrote .audit/findings.json')
