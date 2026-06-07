"""Generate the fingerprint trailer for the report.

We emit:
1. One line per NEW finding with severity + status + rule + file + step + line.
2. One aggregate line per UNCHANGED rule class (rule severity=X status=open count=N files=...)
3. RESOLVED lines for any prior fingerprints that disappeared (0 today).
"""

import json
import hashlib
import os
from collections import defaultdict, Counter

d = json.load(open('.audit/final.json'))
findings = d['findings']

def base(p):
    return os.path.basename(p)

def fp(rule, fname, step):
    s = f"{rule}|{base(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]

new = [f for f in findings if f['delta'] == 'NEW']
unchanged = [f for f in findings if f['delta'] == 'UNCHANGED']

print('# NEW (one fingerprint per finding):')
for f in sorted(new, key=lambda x: (x['severity'], x['file'], x['line'])):
    fp_ = fp(f['short_rule'], f['file'], f['step'])
    status = 'manual' if f['severity'] in ('Critical', 'High') else 'open'
    step_us = f['step'].replace(' ', '_')
    print(f"{fp_} severity={f['severity']} status={status} rule={f['short_rule']} file=.github/workflows/{base(f['file'])} step={step_us} line={f['line']} delta=NEW")

print('\n# UNCHANGED (per-(rule, file) aggregate):')
agg = defaultdict(int)
agg_files = defaultdict(set)
for f in unchanged:
    agg[(f['short_rule'], f['severity'])] += 1
    agg_files[(f['short_rule'], f['severity'])].add(base(f['file']))

for (rule, sev), n in sorted(agg.items()):
    files = ','.join(sorted(agg_files[(rule, sev)]))
    print(f"{rule} severity={sev} status=open count={n} files={files} delta=UNCHANGED")

print('\n# Pinned-uses delta detail:')
upins = [f for f in new if f['short_rule'] == 'unpinned-uses']
for f in upins:
    print(f"  NEW unpinned-uses {base(f['file'])}:{f['line']} step={f['step']!r}")
