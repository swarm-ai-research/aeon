import json, subprocess, os, re
from collections import Counter

d = json.load(open('.audit/classified2.json'))
findings = d['findings']
print('Total today:', len(findings))
print('By delta:', Counter(f['delta'] for f in findings))
sems = [tuple(f['semkey']) for f in findings]
print('Unique semkeys today:', len(set(sems)))
dup_semkeys = [k for k, n in Counter(sems).most_common() if n > 1]
print('Duplicated semkeys count:', len(dup_semkeys))
for k in dup_semkeys[:6]:
    print(' dup semkey:', k, '->', Counter(sems)[k])

# Prior
prior = subprocess.check_output(['git', 'show', 'refs/audit-prior:articles/workflow-security-audit-2026-08-09.md']).decode()
prior_sems = set()
for m in re.finditer(r'^[a-f0-9]{12}\s+severity=\S+\s+status=\S+\s+rule=(\S+)\s+file=(\S+)\s+step=(\S+)\s*$', prior, re.M):
    prior_sems.add((m.group(1), os.path.basename(m.group(2)), m.group(3)))
print('Prior semkeys:', len(prior_sems))
today_sems = set(sems)
print('Today  ∪ Prior:', len(today_sems | prior_sems))
print('Today  ∩ Prior:', len(today_sems & prior_sems))
print('Today \\ Prior:', len(today_sems - prior_sems))
print('Prior \\ Today:', len(prior_sems - today_sems))

# Are prior semkeys collision-free per file?
print()
print('Sample Today-only (would be NEW):')
for s in list(today_sems - prior_sems)[:10]:
    print(' ', s)
print()
print('Sample Prior-only (would be RESOLVED):')
for s in list(prior_sems - today_sems)[:10]:
    print(' ', s)
