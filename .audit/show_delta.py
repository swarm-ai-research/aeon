import json

c = json.load(open('.audit/classified.json'))
current = c['current']
resolved = c['resolved']

print("=== NEW findings ===")
for f in current:
    if f['status'] == 'NEW':
        print(f"  [{f['severity']}] {f['rule_id']}  fp={f['fingerprint']}")
        print(f"     {f['file']}:{f['line']}  step={f['step']!r}")
        if f.get('pattern'):
            snip = f['pattern'].replace('\n', ' ')[:120]
            print(f"     snippet: {snip}")

print()
print("=== RESOLVED (present in prior, absent now) ===")
for f in resolved:
    print(f"  [{f.get('severity','?')}] {f.get('rule','?')} in {f.get('file','?')} step={f.get('step','?')} fp={f['fingerprint']}")
