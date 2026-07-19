import json
with open('.audit/zizmor.sarif') as f:
    sarif = json.load(f)
results = sarif['runs'][0]['results']
for r in results:
    if r.get('ruleId') == 'zizmor/unpinned-uses':
        top_keys = list(r.keys())
        print('top_keys:', top_keys)
        print('properties:', r.get('properties'))
        print('taxa:', r.get('taxa'))
        # look for severity anywhere
        s = json.dumps(r)
        for term in ('severity', 'confidence', 'Confidence', 'Severity'):
            if term in s:
                idx = s.find(term)
                print(f'{term}@{idx}:', s[max(0,idx-30):idx+80])
        break
