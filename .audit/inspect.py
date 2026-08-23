import json

sarif = json.load(open('.audit/zizmor.sarif'))
r = sarif['runs'][0]['results'][0]
for k in ['ruleId', 'level', 'message']:
    print(k, '=', r.get(k))
print('properties:')
print(json.dumps(r.get('properties', {}), indent=2)[:1500])
loc0 = r['locations'][0]
print('location keys:', list(loc0.keys()))
pl = loc0['physicalLocation']
print('artifactLocation:', pl.get('artifactLocation'))
region = pl.get('region', {})
print('region keys:', list(region.keys()))
print('startLine=', region.get('startLine'))
print('logicalLocations=', loc0.get('logicalLocations'))
