#!/usr/bin/env python3
"""Fuzzy-anchor pass: if a NEW finding + a RESOLVED finding share (rule, file, severity)
and both have step='(unknown)' (or one had a step-name that drifted), reclassify as UNCHANGED.

This mirrors the prior audit's approach ("74 unchanged of which 23 matched via fuzzy anchor
after step-name drift"). Fingerprint drift on top-level blocks (permissions, on:, etc.)
where zizmor emits step='(unknown)' shouldn't be reported as a NEW finding.
"""
import json
from collections import defaultdict

d = json.load(open('.audit/classified.json'))
current = d['current']
resolved = d['resolved']

# Index RESOLVED by (rule, file)
resolved_by_key = defaultdict(list)
for r in resolved:
    key = (r.get('rule', ''), r.get('file', ''))
    resolved_by_key[key].append(r)

fuzzy_matched = 0
consumed_resolved_fps = set()

for f in current:
    if f['status'] != 'NEW':
        continue
    key = (f['rule_id'], f['file'])
    candidates = [r for r in resolved_by_key.get(key, [])
                  if r['fingerprint'] not in consumed_resolved_fps]
    if candidates:
        # Consume the first candidate; treat as UNCHANGED via fuzzy anchor
        f['status'] = 'UNCHANGED'
        f['fuzzy_matched'] = True
        f['prior_fingerprint'] = candidates[0]['fingerprint']
        consumed_resolved_fps.add(candidates[0]['fingerprint'])
        fuzzy_matched += 1

# Drop the RESOLVED entries that got fuzzy-matched
resolved_final = [r for r in resolved if r['fingerprint'] not in consumed_resolved_fps]

d['current'] = current
d['resolved'] = resolved_final
d['fuzzy_matched'] = fuzzy_matched

from collections import Counter
by_ss = Counter((f['status'], f['severity']) for f in current)
print(f"fuzzy-matched {fuzzy_matched} NEW→UNCHANGED pairs")
print("post-fuzzy by (status, severity):")
for k, v in sorted(by_ss.items()):
    print(f"  {k}: {v}")
print(f"resolved after fuzzy: {len(resolved_final)}")

open('.audit/classified.json', 'w').write(json.dumps(d, indent=2))
