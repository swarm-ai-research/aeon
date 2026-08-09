import json
from collections import Counter
d = json.load(open('.audit/findings.json'))
uc = Counter(f['severity'] for f in d['unchanged'])
print('unchanged by sev:', dict(uc))
print('unchanged total:', len(d['unchanged']))
print('resolved total:', len(d['resolved']))
print('new total:', len(d['new']))
# Break unchanged by (rule, file) for table
by_rule = Counter(f['rule_id'] for f in d['unchanged'])
print('\nunchanged by rule:')
for k, v in by_rule.most_common():
    print(f'  {v:3d}  {k}')
