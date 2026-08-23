import json

fs = json.load(open('.audit/current.json'))
crit_high = [f for f in fs if f['severity'] in ('Critical', 'High')]
print(f"Critical + High: {len(crit_high)}")
for f in sorted(crit_high, key=lambda x: (x['file'], x['line'])):
    print(f"  [{f['severity']}] {f['rule_id']:35s} fp={f['fingerprint']}")
    print(f"     {f['file']}:{f['line']}  step={f['step']!r}")

# Also inspect the aeon.yml unpinned-uses that should be 3 distinct
print()
print("aeon.yml unpinned findings:")
for f in fs:
    if f['file'] == '.github/workflows/aeon.yml' and 'unpinned' in f['rule_id']:
        print(f"  fp={f['fingerprint']} line={f['line']} step={f['step']!r}")
