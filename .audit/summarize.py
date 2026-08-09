#!/usr/bin/env python3
"""Summarize zizmor SARIF + actionlint JSON."""
import json, hashlib, os, sys
from collections import Counter, defaultdict

sarif = json.load(open('.audit/zizmor.sarif'))
runs = sarif.get('runs', [])
print(f'sarif_runs={len(runs)}')

zizmor_results = runs[0].get('results', []) if runs else []
print(f'zizmor_results={len(zizmor_results)}')

# Load rule metadata to map ruleId -> severity/rule-name for zizmor
rule_meta = {}
if runs:
    for r in runs[0].get('tool', {}).get('driver', {}).get('rules', []):
        rule_meta[r.get('id')] = r

by_rule = Counter()
by_level = Counter()
severity_confidence = Counter()
for r in zizmor_results:
    rid = r.get('ruleId', '?')
    lvl = r.get('level', 'note')
    by_rule[rid] += 1
    by_level[lvl] += 1
    props = r.get('properties', {})
    sev = props.get('problem.severity') or 'unknown'
    conf = props.get('security-severity', 'unknown')
    severity_confidence[(lvl, sev, conf)] += 1

print('\n--- by rule ---')
for k, v in by_rule.most_common():
    print(f'{v:>4}  {k}')
print('\n--- by level ---')
for k, v in by_level.most_common():
    print(f'{v:>4}  {k}')
print('\n--- (level, severity, security-severity) sample ---')
for k, v in list(severity_confidence.most_common())[:20]:
    print(f'{v:>4}  {k}')

print('\n--- sample result 0 ---')
if zizmor_results:
    print(json.dumps(zizmor_results[0], indent=2)[:2000])

# actionlint
if os.path.exists('.audit/actionlint.json'):
    txt = open('.audit/actionlint.json').read().strip()
    if txt:
        aldata = json.loads(txt)
        print(f'\nactionlint_results={len(aldata)}')
        alrules = Counter(x.get('kind', '?') for x in aldata)
        for k, v in alrules.most_common():
            print(f'{v:>4}  {k}')
