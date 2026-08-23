import json
from collections import defaultdict

fs = json.load(open('.audit/parsed.json'))

ti = [f for f in fs if f['rule_id'] == 'zizmor/template-injection']
print(f"total template-injection: {len(ti)}")

zc = defaultdict(int)
for f in ti:
    zc[(f['zsev'], f['zconf'], f['persona'])] += 1
for k, v in zc.items():
    print(k, v)

# Also, hand-inspect a few
for f in ti[:6]:
    print()
    print(f"[{f['severity']}] {f['file']}:{f['line']} route={f['step']}")
    print(f"  zsev={f['zsev']} zconf={f['zconf']} persona={f['persona']}")
    print(f"  msg: {f['message'][:250]}")
    print(f"  snippet: {f['pattern'][:200]!r}")
