#!/usr/bin/env python3
import json, re, os
from collections import Counter, defaultdict

findings = json.load(open('.audit/findings.json'))

prior_path = '.audit-prior/articles/workflow-security-audit-2026-09-06.md'
prior_date = '2026-09-06'
prior_fps = {}
if os.path.exists(prior_path):
    with open(prior_path) as fh:
        text = fh.read()
    m = re.search(r'workflow-security-audit-fingerprints\n(.*?)-->', text, re.DOTALL)
    if m:
        for line in m.group(1).strip().split('\n'):
            parts = line.strip().split()
            if not parts:
                continue
            fp = parts[0]
            attrs = {}
            for p in parts[1:]:
                if '=' in p:
                    k, v = p.split('=', 1)
                    attrs[k] = v
            prior_fps[fp] = attrs
print('prior fingerprints loaded:', len(prior_fps))

current_fps = {f['fingerprint']: f for f in findings}
print('current fingerprints:', len(current_fps))

# Classify
new = []
reintroduced = []
unchanged = []
resolved = []

for fp, f in current_fps.items():
    if fp not in prior_fps:
        f['delta'] = 'NEW'
        new.append(f)
    else:
        prior_status = prior_fps[fp].get('status', '')
        if prior_status in ('auto-fixed', 'resolved'):
            f['delta'] = 'REINTRODUCED'
            reintroduced.append(f)
        else:
            f['delta'] = 'UNCHANGED'
            unchanged.append(f)

for fp, attrs in prior_fps.items():
    if fp not in current_fps:
        resolved.append({'fingerprint': fp, **attrs})

print(f'NEW={len(new)} REINTRODUCED={len(reintroduced)} UNCHANGED={len(unchanged)} RESOLVED={len(resolved)}')
print('NEW by severity:', Counter(f['severity'] for f in new))
print('REINTRODUCED by severity:', Counter(f['severity'] for f in reintroduced))
print('UNCHANGED by severity:', Counter(f['severity'] for f in unchanged))
print('RESOLVED by prior severity:', Counter(a.get('severity','?') for a in resolved))

result = {
    'new': new,
    'reintroduced': reintroduced,
    'unchanged': unchanged,
    'resolved': resolved,
    'prior_date': prior_date,
    'prior_count': len(prior_fps),
    'total': len(findings),
}
with open('.audit/delta.json', 'w') as fh:
    json.dump(result, fh, indent=2)
print('wrote .audit/delta.json')

# Show any NEW findings (if any)
if new:
    print('--- NEW findings ---')
    for f in new[:20]:
        print(f['severity'], f['rule_id'], f['file'], f['step'])
if reintroduced:
    print('--- REINTRODUCED findings ---')
    for f in reintroduced[:20]:
        print(f['severity'], f['rule_id'], f['file'], f['step'])
