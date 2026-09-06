#!/usr/bin/env python3
import json
from collections import Counter

data = json.load(open('.audit/zizmor.sarif'))
runs = data.get('runs', [])
if not runs:
    print('no runs')
else:
    results = runs[0].get('results', [])
    print('total_findings:', len(results))
    by_rule = Counter(r.get('ruleId') for r in results)
    for rule, cnt in by_rule.most_common():
        print(f'  {cnt:4d} {rule}')
    print()
    print('by level:', dict(Counter(r.get('level') for r in results)))
    if results:
        print()
        print('sample record:')
        print(json.dumps(results[0], indent=2)[:1500])
