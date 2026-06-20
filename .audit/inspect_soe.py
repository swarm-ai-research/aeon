import json
findings = json.load(open('.audit/delta_final.json'))['findings']
soe = [f for f in findings if f['short_rule'] == 'secrets-outside-env']
print(f'secrets-outside-env total: {len(soe)}')
seen = set()
for f in soe:
    key = (f['file'], f['step'])
    if key not in seen:
        seen.add(key)
        print()
        print(f"  {f['file']}:{f['line']} step={f['step']!r}")
        print(f"    msg: {f['message'][:200]}")
        print(f"    snippet: {f['snippet'][:200]}")
