#!/usr/bin/env python3
"""Dedup current findings by (rule, file, step), then classify against prior report by tuple.

Fuzzy match: current tuple → prior tuple if (rule, file, step) matches OR
(rule, file, ANY_ALT_STEP) where alt steps include workflow_name / line-fallback /
job-name — handles anchor drift between runs when the step-finder walked a
different distance.
"""
import json, re, os
from collections import Counter, defaultdict

findings = json.load(open('.audit/findings.json'))

# Load workflow files for cross-reference
workflows = {}
for f in os.listdir('.github/workflows'):
    p = f'.github/workflows/{f}'
    if os.path.isfile(p):
        workflows[p] = open(p).read().splitlines()

def workflow_name(path):
    lines = workflows.get(path, [])
    for ln in lines[:10]:
        m = re.match(r'name:\s*(.+)', ln)
        if m:
            return m.group(1).strip().strip('"').strip("'").replace(' ', '_')
    return ''

def short_step(step, line):
    return step.strip().replace(' ', '_') if step else f'line{line}'

# Dedup: one finding per (rule, file, step)
dedup = {}
for f in findings:
    key = (f['rule_id'], f['file'], short_step(f['step'], f['line']))
    if key not in dedup or f['line'] < dedup[key]['line']:
        rec = dict(f)
        rec['step'] = short_step(f['step'], f['line'])
        rec['count'] = dedup.get(key, {}).get('count', 0) + 1
        dedup[key] = rec
    else:
        dedup[key]['count'] = dedup[key].get('count', 1) + 1

deduped = list(dedup.values())
sev_rank = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
deduped.sort(key=lambda x: (sev_rank.get(x['severity'], 9), x['file'], x['line']))
print(f'Deduped findings: {len(deduped)} (from {len(findings)} raw)')
by_sev = Counter(f['severity'] for f in deduped)
for s in ('Critical', 'High', 'Medium', 'Low'):
    print(f'  {s}: {by_sev.get(s, 0)}')

# Parse prior trailer
prior_trailer = []
try:
    prior_text = open('.audit/prior_report.md').read()
    m = re.search(r'workflow-security-audit-fingerprints\n(.*?)(?:\n-->|$)', prior_text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = dict(re.findall(r'(\w+)=(\S+)', line))
            if 'rule' in parts and 'file' in parts and 'step' in parts:
                prior_trailer.append(parts)
    print(f'\nPrior trailer entries: {len(prior_trailer)}')
except FileNotFoundError:
    print('No prior report — bootstrap classification')

# Build prior maps
prior_exact = set()  # (rule, file, step)
prior_by_rule_file = defaultdict(list)  # (rule, file) -> list of step + status
prior_status = {}
for e in prior_trailer:
    key = (e['rule'], e['file'], e['step'])
    prior_exact.add(key)
    prior_by_rule_file[(e['rule'], e['file'])].append(e['step'])
    prior_status[key] = e.get('status', 'manual')

# Fuzzy match: for a current finding, check exact tuple, then check line-fallback
# and workflow-name against prior list for the same (rule, file).
matched_prior = set()
for f in deduped:
    key = (f['rule_id'], f['file'], f['step'])
    if key in prior_exact:
        f['delta'] = ('REINTRODUCED' if prior_status.get(key) in ('auto-fixed', 'resolved') else 'UNCHANGED')
        matched_prior.add(key)
        continue

    # Alt anchors: line-fallback, workflow-name, and the raw step-name-with-underscores
    alt_anchors = [
        f'line{f["line"]}',
        workflow_name(f['file']),
        f['step'],
    ]
    prior_steps = prior_by_rule_file.get((f['rule_id'], f['file']), [])
    matched = None
    for anchor in alt_anchors:
        if anchor and anchor in prior_steps:
            matched = anchor
            break
    if matched:
        prior_key = (f['rule_id'], f['file'], matched)
        f['delta'] = ('REINTRODUCED' if prior_status.get(prior_key) in ('auto-fixed', 'resolved') else 'UNCHANGED')
        matched_prior.add(prior_key)
        f['anchor_drift'] = f"prior step '{matched}' → current step '{f['step']}'"
    else:
        f['delta'] = 'NEW'

# RESOLVED: prior tuples not matched by any current finding (exact or fuzzy)
resolved = []
for e in prior_trailer:
    key = (e['rule'], e['file'], e['step'])
    if key not in matched_prior:
        # Also check: is there any current finding for (rule, file) at all? If yes and it fuzzy-matched
        # a different anchor, this prior entry has been superseded — still count as matched.
        resolved.append({
            'rule_id': e['rule'],
            'file': e['file'],
            'step': e['step'],
            'severity': e.get('severity', 'Medium'),
        })

by_delta = Counter(f['delta'] for f in deduped)
print(f'\nDelta classification:')
for d in ('NEW', 'REINTRODUCED', 'UNCHANGED'):
    print(f'  {d}: {by_delta.get(d, 0)}')
print(f'  RESOLVED: {len(resolved)}')

out = {
    'findings': deduped,
    'resolved': resolved,
    'prior_count': len(prior_trailer),
    'current_count': len(deduped),
    'prior_date': '2026-07-26',
}
open('.audit/classified.json', 'w').write(json.dumps(out, indent=2))

print('\nNEW findings:')
for f in deduped:
    if f['delta'] == 'NEW':
        print(f"  [{f['severity']}] {f['rule_id']} @ {f['file']}:{f['line']} step={f['step']}")
if resolved:
    print('\nRESOLVED:')
    for r in resolved:
        print(f"  [{r['severity']}] {r['rule_id']} @ {r['file']} step={r['step']}")
