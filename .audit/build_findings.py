#!/usr/bin/env python3
"""Build canonical findings set with fingerprints, applying severity mapping and step-context anchoring."""
import json, hashlib, re, os

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]

# Load raw sources
sarif = json.load(open('.audit/zizmor.sarif'))
actionlint_data = json.load(open('.audit/actionlint.json'))
handrolled = json.load(open('.audit/handrolled.json'))

# Preload workflow files to look up step names by line number.
workflow_files = {}
for f in os.listdir('.github/workflows'):
    p = f'.github/workflows/{f}'
    if os.path.isfile(p):
        workflow_files[f] = open(p).read().splitlines()

def find_step_name(filename, line):
    """Walk backwards to find the nearest 'name:' in a step (heuristic anchor)."""
    lines = workflow_files.get(os.path.basename(filename), [])
    if not lines or line <= 0:
        return ''
    # Walk backwards up to 40 lines looking for '- name:' at step level
    for i in range(min(line-1, len(lines)-1), max(0, line-60), -1):
        ln = lines[i]
        m = re.match(r'\s*-\s*name:\s*(.+)', ln)
        if m:
            return m.group(1).strip().strip('"').strip("'")[:60]
        # Also try `name:` at job level
        m2 = re.match(r'\s*name:\s*(.+)', ln)
        if m2 and '-' not in ln.split(':')[0]:
            return m2.group(1).strip().strip('"').strip("'")[:60]
    return ''

def map_severity_zizmor(level, conf, zsev):
    """Skill's map: error+conf>=high=>Critical, error other or warning+conf=high=>High, warning=>Medium, note=>Low."""
    conf_high = (conf or '').lower() in ('high', 'critical')
    if level == 'error' and conf_high:
        return 'Critical'
    if level == 'error':
        return 'High'
    if level == 'warning' and conf_high:
        return 'High'
    if level == 'warning':
        return 'Medium'
    if level == 'note':
        return 'Low'
    return 'Low'

findings = []

# zizmor
for r in sarif['runs'][0]['results']:
    rid = r.get('ruleId', 'zizmor/unknown')
    level = r.get('level', 'note')
    props = r.get('properties', {})
    conf = props.get('zizmor/confidence', 'Low')
    zsev = props.get('zizmor/severity', 'Low')
    sev = map_severity_zizmor(level, conf, zsev)

    loc = r['locations'][0]['physicalLocation']
    file_uri = loc['artifactLocation']['uri']
    file_full = f'.github/workflows/{file_uri}' if not file_uri.startswith('.github/') else file_uri
    region = loc.get('region', {})
    line = region.get('startLine', 0)
    snippet = region.get('snippet', {}).get('text', '') or r['message']['text']
    snippet = snippet.strip().replace('\n', ' ⏎ ')[:120]

    step_name = find_step_name(file_full, line)

    # Fingerprint anchor: rule_id + file + step_name if any else line-context
    anchor = step_name if step_name else f'line{line}'
    fp = sha256(f'{rid}|{file_full}|{anchor}')

    findings.append({
        'fingerprint': fp,
        'severity': sev,
        'rule_id': rid,
        'file': file_full,
        'line': line,
        'step': step_name,
        'pattern': snippet,
        'source': 'zizmor',
        'message': r['message']['text'],
        'zizmor_severity': zsev,
        'zizmor_confidence': conf,
    })

# actionlint
def map_severity_al(entry):
    msg = entry.get('message', '')
    # Security-relevant if SC2086/SC2046 over github.* interpolation
    m = re.search(r'SC(2086|2046)', msg)
    if m:
        # Check the snippet or filepath+line for github.* in nearby lines
        f = entry.get('filepath', '')
        line = entry.get('line', 0)
        if f and line:
            lines = workflow_files.get(os.path.basename(f), [])
            # scan +/- 15 lines around
            slice_ = lines[max(0, line-1):min(len(lines), line+15)]
            for ln in slice_:
                if re.search(r'\$\{\{\s*github\.[a-z_.]+', ln):
                    return 'High'
        return 'Medium'
    return 'Medium'

for e in actionlint_data:
    fp_key = f"actionlint|{e.get('filepath','')}|{re.search(r'SC\\d+', e.get('message','') or '').group(0) if re.search(r'SC\\d+', e.get('message','')) else 'X'}|{e.get('line',0)}"
    fp = sha256(fp_key)
    findings.append({
        'fingerprint': fp,
        'severity': map_severity_al(e),
        'rule_id': 'actionlint/' + (re.search(r'SC\d+', e.get('message','')).group(0) if re.search(r'SC\d+', e.get('message','')) else 'shellcheck'),
        'file': e.get('filepath', ''),
        'line': e.get('line', 0),
        'step': find_step_name(e.get('filepath', ''), e.get('line', 0)),
        'pattern': (e.get('message','') or '')[:120],
        'source': 'actionlint',
        'message': e.get('message', ''),
    })

# hand-rolled
for h in handrolled:
    fp = sha256(f"{h['rule_id']}|{h['file']}|{find_step_name(h['file'], h['line']) or ('line' + str(h['line']))}")
    findings.append({
        'fingerprint': fp,
        'severity': h['severity'],
        'rule_id': h['rule_id'],
        'file': h['file'],
        'line': h['line'],
        'step': find_step_name(h['file'], h['line']),
        'pattern': h['pattern'],
        'source': 'hand-rolled',
        'message': h.get('pattern', ''),
    })

# Sort: severity rank, then file, then line
sev_rank = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
findings.sort(key=lambda x: (sev_rank.get(x['severity'], 9), x['file'], x.get('line', 0)))

print(f'Total findings: {len(findings)}')
from collections import Counter
by_sev = Counter(f['severity'] for f in findings)
for s in ('Critical', 'High', 'Medium', 'Low'):
    print(f'  {s}: {by_sev.get(s, 0)}')

open('.audit/findings.json', 'w').write(json.dumps(findings, indent=2))
