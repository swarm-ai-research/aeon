import json
from collections import defaultdict

fs = json.load(open('.audit/parsed.json'))
pairs = defaultdict(int)
for f in fs:
    pairs[(f['rule_id'], f['level'], f['zsev'], f['zconf'])] += 1

for k, v in sorted(pairs.items()):
    print(f"{v:4d}  rule={k[0]:35s} level={k[1]:10s} zsev={k[2]:14s} zconf={k[3]}")
