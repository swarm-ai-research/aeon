import json
with open('.audit/zizmor.sarif') as f:
    sarif = json.load(f)
r = sarif['runs'][0]['results'][0]
# rule metadata?
rules = sarif['runs'][0].get('tool', {}).get('driver', {}).get('rules', [])
print('num_rules:', len(rules))
for rule in rules:
    if rule.get('id') in ('unpinned-uses', 'zizmor/unpinned-uses'):
        print(json.dumps(rule, indent=2)[:1500])
        print('---')
