import json
import hashlib
from collections import Counter

data = json.load(open('.audit/zizmor.sarif'))

runs = data.get('runs', [])
all_findings = []
for run in runs:
    rules = {r['id']: r for r in run.get('tool', {}).get('driver', {}).get('rules', [])}
    for r in run.get('results', []):
        rule_id = r.get('ruleId', '?')
        level = r.get('level', 'note')
        message = r.get('message', {}).get('text', '')
        props = r.get('properties', {})
        sev = props.get('problem.severity') or props.get('zizmor/severity') or props.get('security-severity', '')
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

print(f'Total zizmor findings: {len(all_findings)}')
print(f'By rule_id:')
for rid, n in Counter(f['rule_id'] for f in all_findings).most_common():
    print(f'  {n:4d}  {rid}')
print(f'\nBy level:')
for l, n in Counter(f['level'] for f in all_findings).most_common():
    print(f'  {n:4d}  {l}')
print(f'\nBy zizmor severity:')
for s, n in Counter(f['severity_zizmor'] for f in all_findings).most_common():
    print(f'  {n:4d}  {s}')
print(f'\nBy confidence:')
for c, n in Counter(f['confidence'] for f in all_findings).most_common():
    print(f'  {n:4d}  {c}')
print(f'\nBy file:')
for fl, n in Counter(f['file'] for f in all_findings).most_common():
    print(f'  {n:4d}  {fl}')

# Write parsed findings to disk
json.dump(all_findings, open('.audit/parsed.json', 'w'), indent=2)
