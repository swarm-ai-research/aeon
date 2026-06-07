import json
import re
import os
import hashlib
from collections import Counter, defaultdict

findings = json.load(open('.audit/parsed.json'))

# Apply severity mapping (re-applied since we save back)
def our_severity(f):
    level = f['level']
    conf = f.get('confidence', '').lower()
    if level == 'error' and conf == 'high':
        return 'Critical'
    if level == 'error':
        return 'High'
    if level == 'warning' and conf == 'high':
        return 'High'
    if level == 'warning':
        return 'Medium'
    return 'Low'

# Normalize file paths: zizmor SARIF gives basenames; resolve to workflow dir
def resolve_path(basename):
    cand1 = os.path.join('.github/workflows', basename)
    if os.path.exists(cand1):
        return cand1
    cand2 = basename  # as-is
    if os.path.exists(cand2):
        return cand2
    return None

# For each unique resolved file, build line -> step map
file_steps = {}
for src in {f['file'] for f in findings}:
    real = resolve_path(src)
    if not real:
        continue
    lines = open(real).readlines()
    step_map = {}
    current_step = 'top'
    for i, line in enumerate(lines, 1):
        m = re.match(r"\s*-\s*name:\s*[\"']?(.+?)[\"']?\s*$", line)
        if m:
            current_step = m.group(1).strip()
        step_map[i] = current_step
    file_steps[src] = step_map

for f in findings:
    fp = file_steps.get(f['file'], {})
    f['step'] = fp.get(f['line'], 'top')
    f['severity'] = our_severity(f)
    f['short_rule'] = f['rule_id'].split('/')[-1]
    fp_src = f"{f['short_rule']}|{f['file']}|{f['step']}"
    f['fingerprint'] = hashlib.sha256(fp_src.encode()).hexdigest()[:16]

# Print summary by (rule, file, step)
c = Counter((f['short_rule'], f['file'], f['step']) for f in findings)
print('Findings per (rule, file, step):')
for (r, fl, st), n in sorted(c.items()):
    print(f'  {n:3d}  {r:25s} {fl:25s} step={st!r}')

print(f'\nUnique fingerprints: {len({f["fingerprint"] for f in findings})}')
print(f'\nSeverity summary:')
for s, n in Counter(f['severity'] for f in findings).most_common():
    print(f'  {n:4d}  {s}')

json.dump(findings, open('.audit/classified.json', 'w'), indent=2)
