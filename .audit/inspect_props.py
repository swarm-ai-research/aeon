#!/usr/bin/env python3
import json
data = json.load(open('.audit/zizmor.sarif'))
results = data['runs'][0]['results']
# examine the properties field structure of a template-injection finding
for r in results:
    if r.get('ruleId') == 'zizmor/template-injection':
        print('level:', r.get('level'))
        print('properties keys:', list(r.get('properties', {}).keys()))
        print('properties:', json.dumps(r.get('properties', {}), indent=2))
        break
print()
print('--- an error-level finding ---')
for r in results:
    if r.get('level') == 'error':
        print('rule:', r.get('ruleId'))
        print('level:', r.get('level'))
        print('properties:', json.dumps(r.get('properties', {}), indent=2))
        break
