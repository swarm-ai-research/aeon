import json
d = json.load(open('.audit/zizmor.sarif'))
r = d['runs'][0]['results']
# Inspect properties for severity fields on the first result of each rule
seen_rules = set()
for x in r:
    rid = x.get('ruleId')
    if rid in seen_rules:
        continue
    seen_rules.add(rid)
    print('==', rid, '==')
    print('  level:', x.get('level'))
    print('  properties:', x.get('properties'))
    print()

# Also inspect the rules section of driver
rules = d['runs'][0]['tool']['driver'].get('rules', [])
print('rule defs:', len(rules))
for ru in rules[:10]:
    print('  id:', ru.get('id'), 'name:', ru.get('name'), 'defaultConfiguration:', ru.get('defaultConfiguration'), 'properties:', ru.get('properties'))
