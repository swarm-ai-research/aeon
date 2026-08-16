"""Build today's audit findings, classify against prior 2026-08-09 audit."""
import json, hashlib, os, re, subprocess
from collections import Counter, defaultdict

TODAY = '2026-08-16'
PRIOR_DATE = '2026-08-09'

# --- Load zizmor SARIF ---
sarif = json.load(open('.audit/zizmor.sarif'))
runs = sarif.get('runs', [])
if not runs:
    raise SystemExit('no zizmor results')

# Load workflow YAML bodies to resolve step names from line numbers
_YAML_CACHE = {}
def _resolve_path(path):
    # If the path has no directory, prefer workflows/actions dir over cwd (zizmor
    # emits basenames like `aeon.yml`, but `aeon.yml` also exists at repo root as
    # the skill schedule — the SARIF one is the workflow file).
    if '/' not in path:
        for prefix in ('.github/workflows/', '.github/actions/'):
            candidate = prefix + path
            if os.path.exists(candidate):
                return candidate
    if os.path.exists(path):
        return path
    for prefix in ('.github/workflows/', '.github/actions/'):
        candidate = prefix + path
        if os.path.exists(candidate):
            return candidate
    return path

def _get_lines(path):
    real = _resolve_path(path)
    if real not in _YAML_CACHE:
        try:
            _YAML_CACHE[real] = open(real).read().splitlines()
        except Exception:
            _YAML_CACHE[real] = []
    return _YAML_CACHE[real]

def resolve_step(file, line):
    """Walk up from line to find nearest `- name:` above."""
    lines = _get_lines(file)
    if not lines or line <= 0 or line > len(lines):
        return '(unknown)'
    for i in range(line-1, -1, -1):
        m = re.match(r'\s*-\s*name:\s*(.+?)\s*$', lines[i])
        if m:
            name = m.group(1).strip('"\'').strip()
            # Skip artifact/upload metadata that isn't a job step
            return name
    return '(unknown)'

findings = []

for run in runs:
    for r in run.get('results', []):
        rule_id = r.get('ruleId', '?')  # e.g. zizmor/unpinned-uses
        level = r.get('level', 'note')
        msg = r.get('message', {}).get('text', '')
        props = r.get('properties', {})
        zizmor_sev = props.get('problem.severity') or props.get('zizmor/severity') or ''
        zizmor_conf = props.get('zizmor/confidence', '')

        locs = r.get('locations', [])
        if not locs:
            continue
        phys = locs[0].get('physicalLocation', {})
        uri = phys.get('artifactLocation', {}).get('uri', '')
        # Normalize to canonical path
        canonical = _resolve_path(uri)
        region = phys.get('region', {})
        line = region.get('startLine', 0)
        snippet = region.get('snippet', {}).get('text', '')

        # First try snippet: zizmor's snippet often starts with `name: <StepName>`
        step = '(unknown)'
        if snippet:
            m = re.match(r'\s*name:\s*(.+?)\s*(?:\n|$)', snippet)
            if m:
                step = m.group(1).strip('"\'').strip()
        if step == '(unknown)':
            step = resolve_step(uri, line)
        uri = canonical

        # Map zizmor -> our severity
        if level == 'error' and zizmor_conf.lower() == 'high':
            sev = 'Critical'
        elif level == 'error':
            sev = 'High'
        elif level == 'warning' and zizmor_conf.lower() == 'high':
            sev = 'High'
        elif level == 'warning':
            sev = 'Medium'
        else:
            sev = 'Low'

        # Calibration: unpinned-uses (Trail-of-Bits treats as error under auditor persona)
        # Prior audits classify these as Critical for actions/* and High otherwise.
        short = rule_id.split('/', 1)[-1]
        if short == 'unpinned-uses':
            # 08-09 report used Critical for aeon.yml actions/* and High for others
            # Preserve that mapping to keep delta stable.
            sev = 'Critical' if uri.endswith('aeon.yml') else 'High'

        # secrets-outside-env: 08-09 report treated as High (env gating)
        if short == 'secrets-outside-env':
            sev = 'High'
        # ref-version-mismatch: 08-09 treated as High
        if short == 'ref-version-mismatch':
            sev = 'High'
        # artipacked: 08-09 treated as Medium
        if short == 'artipacked':
            sev = 'Medium'
        # template-injection: 08-09 treated as Low (audit persona overreports here)
        if short == 'template-injection':
            sev = 'Low'
        # anonymous-definition / undocumented-permissions / concurrency-limits: Low
        if short in ('anonymous-definition', 'undocumented-permissions', 'concurrency-limits'):
            sev = 'Low'

        findings.append({
            'source': 'zizmor',
            'rule_id': rule_id,
            'short': short,
            'severity': sev,
            'file': uri,
            'line': line,
            'step': step,
            'pattern': (snippet.strip()[:120]) if snippet else '',
            'message': msg,
        })

# --- Load actionlint JSON ---
try:
    al = json.load(open('.audit/actionlint.json'))
except Exception:
    al = []

for a in al:
    msg = a.get('message', '')
    file = a.get('filepath', '')
    kind = a.get('kind', 'actionlint')
    # Extract subcode from message: "SC2129:style:..." or "SC2086:info:6:82:..."
    m = re.match(r'shellcheck reported issue in this script: (SC\d+):(\w+):(\d+):(\d+):\s*(.*)', msg)
    if m:
        sc_code = m.group(1)
        sc_level = m.group(2)
        sc_relline = int(m.group(3))
        sc_relcol = int(m.group(4))
        sc_msg = m.group(5)
        rule_id = f'actionlint/{sc_code}'
    else:
        sc_code = kind
        rule_id = f'actionlint/{kind}'
        sc_msg = msg
        sc_relline = 0
        sc_level = 'info'

    line = a.get('line', 0)
    file = _resolve_path(file)
    step = resolve_step(file, line)

    # Severity: Medium default; upgrade to High if SC2086/SC2046 near github.* interpolation
    sev = 'Medium'
    if sc_code in ('SC2086', 'SC2046'):
        # Check the actual line for github.* interpolation
        lines = _get_lines(file)
        # Get the target line (relative to the `run:` block start)
        # Approximation: use snippet region
        # Simpler heuristic: search ±20 lines for github.event / github.head_ref
        start_idx = max(0, line - 5)
        end_idx = min(len(lines), line + 30)
        window = '\n'.join(lines[start_idx:end_idx])
        if re.search(r'\$\{\{\s*github\.(event|head_ref|pull_request|actor|ref)', window):
            sev = 'High'
    # SC2155, SC2129, SC2034 (style/warning) → Low per prior audit
    if sc_code in ('SC2155', 'SC2129', 'SC2034'):
        sev = 'Low'

    findings.append({
        'source': 'actionlint',
        'rule_id': rule_id,
        'short': sc_code,
        'severity': sev,
        'file': file,
        'line': line,
        'step': step,
        'pattern': '',
        'message': sc_msg or msg,
    })

# --- Hand-rolled backstops ---
handrolled_findings = []
for root, _, files in os.walk('.github'):
    for fname in files:
        if not (fname.endswith('.yml') or fname.endswith('.yaml')):
            continue
        path = os.path.join(root, fname)
        try:
            body = open(path).read()
        except Exception:
            continue
        # toJson-into-shell
        for m in re.finditer(r"echo\s+'?\$\{\{\s*toJson\(github\.event", body):
            line = body[:m.start()].count('\n') + 1
            step = resolve_step(path, line)
            handrolled_findings.append({
                'source': 'hand-rolled',
                'rule_id': 'handrolled/tojson-shell-injection',
                'short': 'tojson-shell-injection',
                'severity': 'Critical',
                'file': path,
                'line': line,
                'step': step,
                'pattern': body[m.start():m.start()+120].replace('\n', ' ')[:120],
                'message': 'toJson(github.event.*) interpolated into echo → jq — script injection',
            })
        # persist-credentials true + head.sha checkout on pull_request_target
        # (rough grep, may false-positive)
        if 'pull_request_target' in body and 'persist-credentials' in body:
            for m in re.finditer(r'persist-credentials:\s*true', body):
                line = body[:m.start()].count('\n') + 1
                # confirm nearby head.sha
                window = body[m.start():m.start()+800]
                if re.search(r'ref:\s*\$\{\{\s*github\.event\.pull_request\.head\.(sha|ref)', window):
                    step = resolve_step(path, line)
                    handrolled_findings.append({
                        'source': 'hand-rolled',
                        'rule_id': 'handrolled/pwn-request-poison',
                        'short': 'pwn-request-poison',
                        'severity': 'Critical',
                        'file': path,
                        'line': line,
                        'step': step,
                        'pattern': 'persist-credentials: true + head.sha checkout on pull_request_target',
                        'message': 'poisoned pipeline: writable creds + attacker-controlled ref',
                    })
        # GITHUB_ENV write with user-controlled data
        for m in re.finditer(r'echo\s+"[^"]*\$\{\{\s*github\.event\.[^}]+\}\}[^"]*"\s*>>\s*"?\$GITHUB_(ENV|OUTPUT)', body):
            line = body[:m.start()].count('\n') + 1
            step = resolve_step(path, line)
            handrolled_findings.append({
                'source': 'hand-rolled',
                'rule_id': 'handrolled/github-env-injection',
                'short': 'github-env-injection',
                'severity': 'High',
                'file': path,
                'line': line,
                'step': step,
                'pattern': body[m.start():m.start()+120].replace('\n', ' ')[:120],
                'message': 'GITHUB_ENV / GITHUB_OUTPUT write with user-controlled data — newline injection',
            })

findings.extend(handrolled_findings)

# --- Dedup: same (rule_id, basename(file), step) is one finding ---
# The prior audit collapses multiple raw hits per step into a single finding —
# we follow that convention so counts and semkeys line up 1:1 with the prior trailer.
seen = set()
dedup = []
for f in findings:
    k = (f['rule_id'], os.path.basename(f['file']), f['step'])
    if k in seen:
        continue
    seen.add(k)
    dedup.append(f)
findings = dedup

# --- Fingerprint using prior-audit-compatible key: (rule_id_full, basename(file), step) ---
def fingerprint(f):
    key = f"{f['rule_id']}|{os.path.basename(f['file'])}|{f['step'].replace(' ','_')}"
    return hashlib.sha256(key.encode()).hexdigest()[:12]

for f in findings:
    f['fingerprint'] = fingerprint(f)

# --- Prior audit fingerprints from 08-09 trailer ---
# We can't reproduce the raw hash exactly (unknown algorithm), so we key by
# the SEMANTIC identity: (rule, basename(file), step) — same as our fingerprint input.
prior_trailer_raw = subprocess.check_output(
    ['git', 'show', 'refs/audit-prior:articles/workflow-security-audit-2026-08-09.md']
).decode()

prior_semkeys = set()
prior_records = {}
prior_hash_re = re.compile(
    r'^([a-f0-9]{12})\s+severity=(\w+)\s+status=(\w+)\s+rule=(\S+)\s+file=(\S+)\s+step=(\S+)\s*$',
    re.M
)
for m in prior_hash_re.finditer(prior_trailer_raw):
    fp, sev, status, rule, file, step = m.groups()
    semkey = (rule, os.path.basename(file), step)
    prior_semkeys.add(semkey)
    prior_records[semkey] = {'fp': fp, 'severity': sev, 'status': status, 'rule': rule, 'file': file, 'step': step}

# --- Classify ---
today_semkeys = set()
for f in findings:
    semkey = (f['rule_id'], os.path.basename(f['file']), f['step'].replace(' ', '_'))
    f['semkey'] = semkey
    today_semkeys.add(semkey)
    if semkey in prior_semkeys:
        prev = prior_records[semkey]
        if prev['status'] in ('auto-fixed', 'resolved'):
            f['delta'] = 'REINTRODUCED'
        else:
            f['delta'] = 'UNCHANGED'
    else:
        f['delta'] = 'NEW'

resolved = []
for semkey in prior_semkeys - today_semkeys:
    r = prior_records[semkey]
    resolved.append(r)

# --- Summary ---
sev_c = Counter(f['severity'] for f in findings)
delta_c = Counter(f['delta'] for f in findings)
new_findings = [f for f in findings if f['delta'] == 'NEW']
new_sev = Counter(f['severity'] for f in new_findings)
reintro = [f for f in findings if f['delta'] == 'REINTRODUCED']

summary = {
    'total': len(findings),
    'crit': sev_c['Critical'],
    'high': sev_c['High'],
    'med': sev_c['Medium'],
    'low': sev_c['Low'],
    'new': delta_c['NEW'],
    'unchanged': delta_c['UNCHANGED'],
    'reintroduced': delta_c['REINTRODUCED'],
    'resolved': len(resolved),
    'new_crit': new_sev['Critical'],
    'new_high': new_sev['High'],
    'new_med': new_sev['Medium'],
    'new_low': new_sev['Low'],
}
print(json.dumps(summary, indent=2))
print('\nNEW findings:')
for f in sorted(new_findings, key=lambda x: (x['severity'], x['file'], x['line'])):
    print(f"  [{f['severity']}] {f['rule_id']} {f['file']}:{f['line']} step={f['step']!r}")
print('\nREINTRODUCED findings:')
for f in reintro:
    print(f"  [{f['severity']}] {f['rule_id']} {f['file']}:{f['line']} step={f['step']!r}")
print('\nRESOLVED (present prior, absent today):')
for r in resolved:
    print(f"  [{r['severity']}] {r['rule']} {r['file']} step={r['step']!r}")

json.dump({
    'findings': findings,
    'resolved': resolved,
    'summary': summary,
    'today': TODAY,
    'prior_date': PRIOR_DATE,
}, open('.audit/classified2.json', 'w'), indent=2)
