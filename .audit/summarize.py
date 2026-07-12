import json
from collections import Counter
d = json.load(open('.audit/classified.json'))
new = [x for x in d['findings'] if x['classification']=='NEW']
c = Counter(x['file'] for x in new)
for f, n in c.most_common():
    print(f'  {n:3d}  {f}')
print('total NEW:', len(new))
by_rule = Counter(x['rule_id'] for x in new)
print('by rule:')
for k, v in by_rule.most_common():
    print(f'  {v:3d}  {k}')
