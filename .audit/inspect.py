import json
with open('.audit/zizmor.sarif') as f:
    sarif = json.load(f)
results = sarif['runs'][0]['results']
for r in results:
    if r.get('ruleId') == 'unpinned-uses':
        print('ruleId:', r.get('ruleId'))
        print('level:', r.get('level'))
        print('properties:', json.dumps(r.get('properties', {}), indent=2)[:600])
        print('---')
        break
rules_seen = {}
for r in results:
    rid = r.get('ruleId', '?')
    lvl = r.get('level', '?')
    props = r.get('properties', {}) or {}
    prob = props.get('problem.severity') or props.get('security-severity') or '?'
    rules_seen[(rid, lvl, str(prob))] = rules_seen.get((rid, lvl, str(prob)), 0) + 1
print('rules by (ruleId, level, severity):')
for k, v in sorted(rules_seen.items(), key=lambda kv: -kv[1]):
    print(f'  {v:3d}  {k}')
