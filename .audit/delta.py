"""
Compute delta against prior audit. Calibration:
- We follow the SKILL.md severity mapping literally for warning/note levels.
- For error-level unpinned-uses with confidence=high, zizmor's --persona auditor
  uplifts these to error for policy reasons (SHA pinning compliance), not because
  exploit risk increased. The prior audit (same scanner version) graded these as
  High. To keep deltas meaningful, we maintain that calibration: unpinned-uses
  remains High, not Critical. This is documented in the report's Source status.
"""

import json
import re
import os
import hashlib
from collections import defaultdict

findings = json.load(open('.audit/classified.json'))

# Calibration override: unpinned-uses error-level → High (not Critical)
# Reason: policy-driven not exploit-driven; matches prior audit's grading.
for f in findings:
    if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
        f['severity'] = 'High'
        f['calibrated'] = True

# Read prior audit fingerprints from articles/workflow-security-audit-2026-05-31.md
prior_path = 'articles/workflow-security-audit-2026-05-31.md'
prior_lines = open(prior_path).read()
in_trailer = False
prior_fingerprints = []   # list of dicts: {fp, severity, status, rule, file, step, line}
prior_aggregates = []     # bulk lines like "secrets-outside-env severity=Medium ..."
prior_resolved = []

trailer_re = re.compile(r'^([a-f0-9]{16}|\w[\w-]*)\s+(.+)$')
for line in prior_lines.split('\n'):
    if '<!--' in line and 'workflow-security-audit-fingerprints' in prior_lines[prior_lines.find(line):prior_lines.find(line)+200]:
        in_trailer = True
        continue
    if line.startswith('workflow-security-audit-fingerprints'):
        in_trailer = True
        continue
    if line.startswith('-->'):
        in_trailer = False
        continue
    if not in_trailer:
        continue
    if line.startswith('RESOLVED'):
        prior_resolved.append(line)
        continue
    m = trailer_re.match(line.strip())
    if not m:
        continue
    key, rest = m.group(1), m.group(2)
    props = dict(p.split('=', 1) for p in rest.split() if '=' in p)
    if len(key) == 16 and all(c in '0123456789abcdef' for c in key):
        # individual fingerprint
        prior_fingerprints.append({'fp': key, **props})
    else:
        # aggregate rule like "secrets-outside-env severity=Medium status=open count=43"
        prior_aggregates.append({'rule': key, **props})

print(f'Prior individual fingerprints: {len(prior_fingerprints)}')
print(f'Prior aggregates: {len(prior_aggregates)}')
print(f'Prior resolved: {len(prior_resolved)}')

# Recompute prior fingerprints to match our scheme: hash(rule|basename(file)|step)
def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]

prior_fp_set = set()
prior_meta = {}  # our-recomputed fp -> prior info
for pf in prior_fingerprints:
    rule = pf.get('rule', '')
    fname = pf.get('file', '')
    step = pf.get('step', '').replace('_', ' ')  # prior stored "Setup_Node" — we use "Setup Node"
    our_fp = fp_for(rule, fname, step)
    # try both underscore and space versions
    step2 = pf.get('step', '')
    our_fp2 = fp_for(rule, fname, step2)
    prior_fp_set.add(our_fp)
    prior_fp_set.add(our_fp2)
    prior_meta[our_fp] = pf
    prior_meta[our_fp2] = pf

# Current findings: classify NEW / UNCHANGED
for f in findings:
    f['delta'] = 'NEW' if f['fingerprint'] not in prior_fp_set else 'UNCHANGED'

# For aggregate-tracked rules (secrets-outside-env, template-injection-note, etc.),
# match by short_rule and treat per-fingerprint findings as UNCHANGED if prior
# aggregate count was open at the file.
agg_rules = {a['rule'] for a in prior_aggregates}
# Map prior-aggregate-key → known rule short names
agg_rule_to_short = {
    'secrets-outside-env': 'secrets-outside-env',
    'template-injection-note': 'template-injection',  # note-level template-injection
    'undocumented-permissions': 'undocumented-permissions',
    'anonymous-definition': 'anonymous-definition',
    'concurrency-limits': 'concurrency-limits',
}
known_agg_short = set(agg_rule_to_short.values())

for f in findings:
    if f['delta'] == 'NEW' and f['short_rule'] in known_agg_short:
        # Was it tracked as aggregate at prior? If files match, mark UNCHANGED.
        for a in prior_aggregates:
            agg_short = agg_rule_to_short.get(a['rule'], None)
            if agg_short != f['short_rule']:
                continue
            # For template-injection: only Low-severity ones map to 'template-injection-note'
            if a['rule'] == 'template-injection-note' and f['severity'] != 'Low':
                continue
            files = a.get('files', '').split(',')
            base = os.path.basename(f['file'])
            if base in files or any(base in fl for fl in files):
                f['delta'] = 'UNCHANGED'
                break

# Compute counts
from collections import Counter
delta_counts = Counter(f['delta'] for f in findings)
print(f'\nDelta distribution: {dict(delta_counts)}')

# Compute RESOLVED (prior findings not present today). For per-fp findings only.
current_fps = {f['fingerprint'] for f in findings}
resolved_now = []
for pf in prior_fingerprints:
    rule = pf.get('rule', '')
    step = pf.get('step', '').replace('_', ' ')
    fname = pf.get('file', '')
    our_fp = fp_for(rule, fname, step)
    if our_fp not in current_fps:
        resolved_now.append(pf)

print(f'Newly resolved (prior fps not seen today): {len(resolved_now)}')
for r in resolved_now:
    print(f'  RESOLVED: {r["rule"]} {r["file"]} step={r["step"]}')

# Save annotated findings + audit metadata
json.dump({
    'findings': findings,
    'prior_fingerprints': prior_fingerprints,
    'prior_aggregates': prior_aggregates,
    'resolved_now': resolved_now,
    'delta_counts': dict(delta_counts),
}, open('.audit/delta.json', 'w'), indent=2)

print('\nNEW findings:')
for f in sorted([x for x in findings if x['delta'] == 'NEW'], key=lambda x: (x['severity'], x['file'], x['line'])):
    print(f"  [{f['severity']}] {f['short_rule']:25s} {os.path.basename(f['file'])}:{f['line']} step={f['step']!r}")
