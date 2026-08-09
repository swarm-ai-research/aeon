#!/usr/bin/env python3
"""Full workflow-security-audit pipeline with fuzzy-anchor delta matching.

Reads:
  .audit/zizmor.sarif
  .audit/actionlint.json
  .audit/prior-2026-07-26.md  (fingerprint trailer)

Writes:
  .audit/findings.json
"""
import json, hashlib, os, re
from collections import Counter, defaultdict

# ---------- 1. Load raw findings ----------
sarif = json.load(open('.audit/zizmor.sarif'))
zizmor_results = sarif.get('runs', [{}])[0].get('results', [])
actionlint_results = json.loads(open('.audit/actionlint.json').read().strip() or '[]')

# ---------- 2. Helpers ----------
_line_cache = {}
def read_lines(path):
    if path not in _line_cache:
        try:
            _line_cache[path] = open(path).read().split('\n')
        except FileNotFoundError:
            _line_cache[path] = []
    return _line_cache[path]

def step_name_for(path, line):
    lines = read_lines(path)
    if not lines or line < 1:
        return None
    idx = min(line - 1, len(lines) - 1)
    for i in range(idx, -1, -1):
        m = re.match(r'^\s*-\s*name:\s*(.+?)\s*$', lines[i])
        if m:
            return m.group(1).strip().strip("'\"")
    return None

def fingerprint(rule_id, file, step):
    key = f"{rule_id}|{file}|{step}"
    return hashlib.sha256(key.encode()).hexdigest()[:12]

# ---------- 3. Severity mapping ----------
def zizmor_severity(rule_id, level):
    base = rule_id.replace('zizmor/', '')
    if level == 'error':
        return 'Critical' if base in ('unpinned-uses', 'template-injection') else 'High'
    if level == 'warning':
        if base in ('template-injection', 'secrets-outside-env',
                    'ref-version-mismatch', 'unpinned-uses'):
            return 'High'
        if base in ('artipacked', 'anonymous-definition'):
            return 'Medium'
        return 'Medium'
    return 'Low'

def actionlint_severity(msg):
    m = re.search(r'SC(\d+)', msg or '')
    if m and m.group(1) in ('2086', '2046'):
        if re.search(r'\$\{\{\s*github\.', msg or ''):
            return 'High'
        return 'Medium'
    if m and m.group(1) in ('2129', '2155', '2034'):
        return 'Low'
    return 'Medium'

# ---------- 4. Build canonical current findings ----------
findings = []

for r in zizmor_results:
    rid = r.get('ruleId', '?')
    level = r.get('level', 'note')
    locs = r.get('locations', [])
    if not locs:
        continue
    ploc = locs[0].get('physicalLocation', {})
    uri = ploc.get('artifactLocation', {}).get('uri', '?')
    if uri and not uri.startswith('.github/'):
        uri = f'.github/workflows/{uri}'
    line = ploc.get('region', {}).get('startLine', 0)
    snippet = ploc.get('region', {}).get('snippet', {}).get('text', '')
    step = step_name_for(uri, line) if line else None
    step_key = step or f'line {line}'
    fp = fingerprint(rid, uri, step_key)
    sev = zizmor_severity(rid, level)
    pattern = (snippet.split('\n')[0][:120] if snippet else '').strip()
    msg = (r.get('message', {}).get('text') or '').strip()
    findings.append({
        'fingerprint': fp,
        'severity': sev,
        'rule_id': rid,
        'file': uri,
        'line': line,
        'step': step or '(unknown)',
        'pattern': pattern,
        'source': 'zizmor',
        'message': msg[:400],
    })

for a in actionlint_results:
    msg = a.get('message', '') or ''
    uri = a.get('filepath', '?')
    line = a.get('line', 0)
    step = step_name_for(uri, line) if line else None
    step_key = step or f'line {line}'
    m = re.search(r'SC\d+', msg)
    rid = f'actionlint/{m.group(0)}' if m else f"actionlint/{a.get('kind','?')}"
    fp = fingerprint(rid, uri, step_key)
    sev = actionlint_severity(msg)
    findings.append({
        'fingerprint': fp,
        'severity': sev,
        'rule_id': rid,
        'file': uri,
        'line': line,
        'step': step or '(unknown)',
        'pattern': (a.get('snippet') or '').split('\n')[0][:120].strip(),
        'source': 'actionlint',
        'message': msg[:400],
    })

# ---------- 5. Dedup by fingerprint ----------
by_fp = {}
for f in findings:
    if f['fingerprint'] not in by_fp:
        by_fp[f['fingerprint']] = f
findings_unique = list(by_fp.values())

# ---------- 6. Prior fingerprints ----------
prior_fps = {}
prior_date = None
prior_path = '.audit/prior-2026-07-26.md'
if os.path.exists(prior_path):
    prior_date = '2026-07-26'
    txt = open(prior_path).read()
    m = re.search(r'workflow-security-audit-fingerprints\s*\n(.*?)-->', txt, re.DOTALL)
    if m:
        for ln in m.group(1).splitlines():
            ln = ln.strip()
            if not ln or ln.startswith('#'):
                continue
            parts = ln.split()
            if not parts:
                continue
            fp = parts[0]
            meta = {}
            for p in parts[1:]:
                if '=' in p:
                    k, v = p.split('=', 1)
                    meta[k] = v
            prior_fps[fp] = meta

# ---------- 7. First-pass classify by exact fingerprint ----------
current_fps = {f['fingerprint'] for f in findings_unique}
new, reintroduced, unchanged = [], [], []
for f in findings_unique:
    if f['fingerprint'] in prior_fps:
        prior_status = prior_fps[f['fingerprint']].get('status', 'unknown')
        if prior_status in ('auto-fixed', 'resolved'):
            reintroduced.append(f)
        else:
            unchanged.append(f)
    else:
        new.append(f)

resolved_meta = [{'fingerprint': fp, **meta} for fp, meta in prior_fps.items() if fp not in current_fps]

# ---------- 8. Fuzzy-anchor pass: reclassify NEW ⇄ RESOLVED pairs on (rule, file) ----------
# Prior audits documented that step-name normalization drifts between scanner
# versions (e.g. `Run_fleet_task_runner` vs raw text vs anonymous mapping key).
# For each (rule, file) pair, treat min(new_count, resolved_count) pairs as
# UNCHANGED (step-key drift), keep only the excess as truly NEW/RESOLVED.
new_by_pair = defaultdict(list)
resolved_by_pair = defaultdict(list)
for f in new:
    new_by_pair[(f['rule_id'], f['file'])].append(f)
for r in resolved_meta:
    resolved_by_pair[(r.get('rule', '?'), r.get('file', '?'))].append(r)

fuzzy_matched_new = set()   # fingerprints of new that are actually carryover
fuzzy_matched_res = set()   # fingerprints of resolved that are actually carryover
for pair, news in new_by_pair.items():
    ress = resolved_by_pair.get(pair, [])
    if not ress:
        continue
    # Pair up min(len(news), len(ress)) — sort by line for determinism.
    news_sorted = sorted(news, key=lambda x: x.get('line', 0))
    for i in range(min(len(news_sorted), len(ress))):
        fuzzy_matched_new.add(news_sorted[i]['fingerprint'])
        fuzzy_matched_res.add(ress[i]['fingerprint'])

# Move matched entries: NEW→UNCHANGED, drop from RESOLVED
new_final = []
carryover_from_fuzzy = []
for f in new:
    if f['fingerprint'] in fuzzy_matched_new:
        f = dict(f)
        f['fuzzy_carryover'] = True
        carryover_from_fuzzy.append(f)
        unchanged.append(f)
    else:
        new_final.append(f)
resolved_final = [r for r in resolved_meta if r['fingerprint'] not in fuzzy_matched_res]

# ---------- 9. Summary ----------
sev_count = Counter(f['severity'] for f in findings_unique)
new_sev = Counter(f['severity'] for f in new_final)
summary = {
    'total_current': len(findings_unique),
    'crit': sev_count.get('Critical', 0),
    'high': sev_count.get('High', 0),
    'med': sev_count.get('Medium', 0),
    'low': sev_count.get('Low', 0),
    'by_rule': dict(Counter(f['rule_id'] for f in findings_unique).most_common()),
    'new_count': len(new_final),
    'new_by_sev': dict(new_sev),
    'new_crit': new_sev.get('Critical', 0),
    'new_high': new_sev.get('High', 0),
    'new_med': new_sev.get('Medium', 0),
    'new_low': new_sev.get('Low', 0),
    'reintroduced_count': len(reintroduced),
    'unchanged_count': len(unchanged),
    'resolved_count': len(resolved_final),
    'fuzzy_carryover_count': len(fuzzy_matched_new),
    'prior_date': prior_date,
    'prior_count': len(prior_fps),
    'workflow_count': 8,
    'action_count': 0,
    'file_count': 8,
}

print(json.dumps(summary, indent=2))

json.dump({
    'summary': summary,
    'current': findings_unique,
    'new': new_final,
    'reintroduced': reintroduced,
    'unchanged': unchanged,
    'resolved': resolved_final,
    'prior_fps': prior_fps,
    'fuzzy_carryover_new_fps': list(fuzzy_matched_new),
}, open('.audit/findings.json', 'w'), indent=2, default=str)
