import json
from collections import defaultdict

al = json.load(open('.audit/actionlint.json'))
print(f"actionlint entries: {len(al)}")
grouped = defaultdict(int)
for e in al:
    grouped[e.get('kind', 'unknown')] += 1
print("by kind:")
for k, v in grouped.items():
    print(f"  {v:4d} {k}")

# Show samples
for e in al[:8]:
    fp = e.get('filepath', '?')
    line = e.get('line', 0)
    col = e.get('column', 0)
    msg = e.get('message', '')
    kind = e.get('kind', '')
    print(f"  {fp}:{line}:{col}  [{kind}] {msg[:180]}")
