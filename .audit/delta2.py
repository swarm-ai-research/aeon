"""
Delta computation v2: file-level count diff, not step-name match.
Step names were refactored ('Checkout' -> 'Checkout repo') between audits.
"""

import json
import re
import os
import hashlib
from collections import Counter, defaultdict

findings = json.load(open('.audit/classified.json'))

# Calibration: unpinned-uses error-level (zizmor --persona auditor uplifts) -> High,
# not Critical. Matches prior audit's grading; policy-driven, not exploit-driven.
for f in findings:
    if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
        f['severity'] = 'High'
        f['calibrated'] = True

# Parse prior trailer fingerprints + aggregates from prior report
prior_path = 'articles/workflow-security-audit-2026-05-31.md'
text = open(prior_path).read()

prior_indiv = []          # individual prior fingerprints
prior_aggregates = []     # aggregate prior entries
prior_resolved_lines = []
# Extract the trailer
m = re.search(r'<!--\s*\nworkflow-security-audit-fingerprints\n(.*?)\n-->', text, re.DOTALL)
trailer = m.group(1) if m else ''
for raw in trailer.split('\n'):
    line = raw.strip()
    if not line:
        continue
    if line.startswith('RESOLVED'):
        prior_resolved_lines.append(line)
        continue
    parts = line.split()
    head = parts[0]
    props = dict(p.split('=', 1) for p in parts[1:] if '=' in p)
    if len(head) == 16 and all(c in '0123456789abcdef' for c in head):
        prior_indiv.append({'fp': head, **props})
    else:
        prior_aggregates.append({'rule': head, **props})

# Convert prior per-(rule, file) counts to a dict
def short_rule(s):
    return s.split('/')[-1]
def base(p):
    return os.path.basename(p)

prior_counts = Counter()
for pf in prior_indiv:
    r = pf['rule']
    fname = base(pf.get('file', ''))
    prior_counts[(r, fname)] += 1
for a in prior_aggregates:
    rmap = {
        'secrets-outside-env': 'secrets-outside-env',
        'template-injection-note': 'template-injection',
        'undocumented-permissions': 'undocumented-permissions',
        'anonymous-definition': 'anonymous-definition',
        'concurrency-limits': 'concurrency-limits',
    }
    actual_rule = rmap.get(a['rule'], a['rule'])
    files = a.get('files', '').split(',')
    count_per_file = {}
    # crude — total count not split by file in the aggregate string;
    # use file list, distributing count evenly by file presence (approx)
    total = int(a.get('count', 0))
    if not files or files == ['']:
        continue
    # Use prior detail: parse "(N)" suffix where present from the report body
    # — for now treat aggregate as "at least 1 finding per listed file"
    for fl in files:
        if fl:
            prior_counts[(actual_rule, fl)] += 1

# Today's per-(rule, file) counts
today_counts = Counter((f['short_rule'], base(f['file'])) for f in findings)

# Compute deltas at (rule, file) granularity
delta_per_pair = {}
for key in set(today_counts) | set(prior_counts):
    t = today_counts.get(key, 0)
    p = prior_counts.get(key, 0)
    delta_per_pair[key] = {'today': t, 'prior': p, 'diff': t - p}

print('Per-(rule, file) delta:')
for (rule, fname), d in sorted(delta_per_pair.items(), key=lambda x: (-abs(x[1]['diff']), x[0])):
    marker = ''
    if d['diff'] > 0:
        marker = f"  +{d['diff']} NEW"
    elif d['diff'] < 0:
        marker = f"  {d['diff']} RESOLVED"
    print(f'  {rule:28s} {fname:30s} today={d["today"]:3d} prior={d["prior"]:3d}{marker}')

# Now assign per-finding NEW vs UNCHANGED:
# - For each (rule, file) pair, mark first `prior_count` findings as UNCHANGED,
#   the rest as NEW. Order by line ascending so earlier-in-file = more likely old.
new_findings = []
unchanged_findings = []
for (rule, fname), pair_findings in (
    (k, sorted([f for f in findings if (f['short_rule'], base(f['file'])) == k],
               key=lambda x: x['line']))
    for k in {(f['short_rule'], base(f['file'])) for f in findings}
):
    p = prior_counts.get((rule, fname), 0)
    for i, f in enumerate(pair_findings):
        if i < p:
            f['delta'] = 'UNCHANGED'
            unchanged_findings.append(f)
        else:
            f['delta'] = 'NEW'
            new_findings.append(f)

# RESOLVED: pairs where prior > today
resolved_pairs = [(k, d) for k, d in delta_per_pair.items() if d['diff'] < 0]
total_resolved = sum(-d['diff'] for _, d in resolved_pairs)

# Note about prior aggregates: secrets-outside-env had count=43 in prior (single bucket)
# Today's secrets-outside-env total = 44. Net +1 NEW across files.
agg_now = {
    'secrets-outside-env': sum(1 for f in findings if f['short_rule'] == 'secrets-outside-env'),
    'template-injection': sum(1 for f in findings if f['short_rule'] == 'template-injection'),
    'undocumented-permissions': sum(1 for f in findings if f['short_rule'] == 'undocumented-permissions'),
    'anonymous-definition': sum(1 for f in findings if f['short_rule'] == 'anonymous-definition'),
    'concurrency-limits': sum(1 for f in findings if f['short_rule'] == 'concurrency-limits'),
}
agg_prior = {a['rule']: int(a.get('count', 0)) for a in prior_aggregates}

print('\nAggregate-class totals (rule -> today / prior):')
for k, v in agg_now.items():
    pkey = {
        'template-injection': 'template-injection-note',
    }.get(k, k)
    p = agg_prior.get(pkey, 0)
    diff = v - p
    print(f'  {k:30s} today={v:3d} prior={p:3d} diff={diff:+d}')

print('\nCurrent delta:')
print(f'  NEW={len(new_findings)} UNCHANGED={len(unchanged_findings)} RESOLVED~={total_resolved}')

print('\nNEW findings (sorted by severity):')
sev_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
for f in sorted(new_findings, key=lambda x: (sev_order[x['severity']], x['file'], x['line'])):
    print(f'  [{f["severity"]}] {f["short_rule"]:25s} {base(f["file"])}:{f["line"]} step={f["step"]!r}')

# Save final delta
json.dump({
    'findings': findings,
    'delta_summary': {
        'NEW': len(new_findings),
        'UNCHANGED': len(unchanged_findings),
        'RESOLVED_approx': total_resolved,
    },
    'per_pair_delta': {f'{r}|{f_}': d for (r, f_), d in delta_per_pair.items()},
    'agg_now': agg_now,
    'agg_prior': agg_prior,
    'resolved_pairs': [(k, d) for k, d in resolved_pairs],
}, open('.audit/delta_final.json', 'w'), indent=2)
