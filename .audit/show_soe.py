import json, os
d = json.load(open('.audit/findings.json'))
sec = [f for f in d['current'] if f['rule_id'] == 'zizmor/secrets-outside-env']
for f in sec:
    print(f"{os.path.basename(f['file'])}:{f['line']}  step={f['step']!r}")
    print(f"  pattern: {f['pattern']}")
    print(f"  msg: {f['message'][:220]}")
    print()
