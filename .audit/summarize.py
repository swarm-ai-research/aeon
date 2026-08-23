import json
from collections import defaultdict

fs = json.load(open('.audit/parsed.json'))

print("=" * 70)
print("CRITICAL findings:")
print("=" * 70)
for f in fs:
    if f['severity'] == 'Critical':
        print(f"\n[{f['rule_id']}] {f['file']}:{f['line']}")
        print(f"  route: {f['step']}")
        print(f"  zsev={f['zsev']} zconf={f['zconf']} persona={f['persona']}")
        print(f"  msg: {f['message'][:300]}")
        print(f"  snippet: {f['pattern'][:150]!r}")

print()
print("=" * 70)
print("HIGH findings by rule:")
print("=" * 70)
groups = defaultdict(list)
for f in fs:
    if f['severity'] == 'High':
        groups[f['rule_id']].append(f)

for rule, items in sorted(groups.items(), key=lambda x: -len(x[1])):
    print(f"\n== {rule} ({len(items)} findings) ==")
    # Group by file
    by_file = defaultdict(list)
    for i in items:
        by_file[i['file']].append(i)
    for fn, its in sorted(by_file.items()):
        print(f"  {fn}: {len(its)}")
        for i in its[:3]:
            print(f"    line {i['line']} route={i['step']!r}")
            print(f"      msg: {i['message'][:200]}")

print()
print("=" * 70)
print("MEDIUM by rule (compact):")
print("=" * 70)
med_groups = defaultdict(int)
for f in fs:
    if f['severity'] == 'Medium':
        med_groups[f['rule_id']] += 1
for k, v in sorted(med_groups.items(), key=lambda x: -x[1]):
    print(f"  {v:3d} {k}")
