#!/usr/bin/env python3
"""Build canonical findings from zizmor + actionlint outputs.

Fingerprint anchor: (rule_id, file, step_name_or_line). Uses step name from
the SARIF region snippet when detectable (first `name:` in the snippet block);
falls back to `L{line}` when no `name:` found.
"""
import json, hashlib, os, re
from collections import Counter

REPO_NAME = os.environ.get('REPO_NAME', 'aeon-framework/aeon')
REPO_URL = os.environ.get('REPO_URL', f"https://github.com/{os.environ.get('REPO_NAME', 'aeon-framework/aeon')}")

def sev_from_zizmor(r):
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

STEP_NAME_RE = re.compile(r'^\s*(?:-\s+)?name:\s*(.+?)\s*$', re.MULTILINE)

def extract_step_name(snippet: str) -> str | None:
    if not snippet:
        return None
    m = STEP_NAME_RE.search(snippet)
    if m:
        return m.group(1).strip().strip('"\'')
    return None

def normalize_file(uri: str) -> str:
    if '/' not in uri and uri.endswith(('.yml', '.yaml')):
        return f".github/workflows/{uri}"
    return uri

def fp(rule, fileuri, ctx):
    return hashlib.sha256(f"{rule}|{fileuri}|{ctx}".encode()).hexdigest()[:16]

findings = []

# --- zizmor ---
sarif = json.load(open('.audit/zizmor.sarif'))
for r in sarif['runs'][0]['results']:
    rule = r.get('ruleId', '?')
    sev = sev_from_zizmor(r)
    loc = r['locations'][0]['physicalLocation']
    fileuri = normalize_file(loc['artifactLocation']['uri'])
    region = loc.get('region', {})
    start_line = region.get('startLine', 0)
    end_line = region.get('endLine', start_line)
    snippet_text = region.get('snippet', {}).get('text', '')
    step_name = extract_step_name(snippet_text)
    ctx = step_name if step_name else f"L{start_line}"
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
        'sarif_severity': r.get('properties', {}).get('zizmor/severity'),
        'msg': r['message']['text'],
        'snippet': snippet_text[:400],
        'source': 'zizmor',
    })

# --- actionlint ---
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
    kind = a.get('kind', '?')
    rule = f"actionlint/{kind}"
    fileuri = a.get('filepath', '?')
    line = a.get('line', 0)
    # actionlint doesn't include step name — use line + rule
    # For shellcheck, extract SC code for stability
    sc = ''
    m = re.search(r'(SC\d+)', a.get('message', ''))
    if m:
        sc = m.group(1)
    ctx = f"{sc}:L{line}" if sc else f"L{line}"
    findings.append({
        'fingerprint': fp(kind, fileuri, ctx),
        'severity': sev_from_actionlint(a),
        'rule_id': f"{rule}/{sc}" if sc else rule,
        'file': fileuri,
        'line': line,
        'end_line': line,
        'step': ctx,
        'step_name': None,
        'msg': a.get('message', ''),
        'snippet': a.get('snippet', '')[:400],
        'source': 'actionlint',
    })

# --- hand-rolled checks ---
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
# toJson piped/substituted into shell — the April 11 miss
tojson_shell_pat = re.compile(
    r"(?:echo|printf)\s+[\"']?\$\{\{\s*toJson\("
)
persist_pat = re.compile(r'persist-credentials:\s*true')
# GITHUB_ENV/OUTPUT direct sink of github.event.*
env_pat = re.compile(r'>>\s*"?\$\{?GITHUB_(?:ENV|OUTPUT)\}?"?')
gh_event_direct_pat = re.compile(r'\$\{\{\s*github\.event\.[^}]+\}\}')
# Mutable third-party ref (owner not in trusted set)
uses_ref_pat = re.compile(
    r'^\s*(?:-\s+)?uses:\s+([A-Za-z0-9._-]+)/([A-Za-z0-9._/-]+)@([A-Za-z0-9._-]+)',
    re.MULTILINE,
)
TRUSTED_OWNERS = {'actions', 'github', 'docker', 'aws-actions'}

for f in workflows:
    if not os.path.exists(f):
        continue
    with open(f) as fh:
        text = fh.read()
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
        if owner in TRUSTED_OWNERS:
            continue
        # SHA pin is 40 hex chars; anything else is mutable
        if not re.fullmatch(r'[0-9a-f]{40}', ref):
            line = text[:m.start()].count('\n') + 1
            handrolled.append((
                'handrolled/mutable-third-party-ref', 'Medium', f, line,
                f'uses: {owner}/{name}@{ref}'[:200],
            ))

for rule, sev, fileuri, line, snippet in handrolled:
    ctx = f"L{line}"
    findings.append({
        'fingerprint': fp(rule, fileuri, ctx),
        'severity': sev,
        'rule_id': rule,
        'file': fileuri,
        'line': line,
        'end_line': line,
        'step': ctx,
        'step_name': None,
        'msg': snippet,
        'snippet': snippet,
        'source': 'hand-rolled',
    })

sev_counts = Counter(f['severity'] for f in findings)
src_counts = Counter(f['source'] for f in findings)
print('total findings:', len(findings))
print('by severity:', dict(sev_counts))
print('by source:', dict(src_counts))
print('hand-rolled findings:', len(handrolled))

with open('.audit/findings_final.json', 'w') as fh:
    json.dump(findings, fh, indent=2)
print('wrote .audit/findings_final.json')
