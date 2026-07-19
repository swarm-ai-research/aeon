import json
with open('.audit/zizmor.sarif') as f:
    sarif = json.load(f)
for r in sarif['runs'][0]['results']:
    if r.get('ruleId') == 'zizmor/unpinned-uses':
        loc = (r.get('locations') or [{}])[0]
        pl = loc.get('physicalLocation') or {}
        art = (pl.get('artifactLocation') or {}).get('uri', '')
        region = pl.get('region') or {}
        line = region.get('startLine')
        snippet = (region.get('snippet') or {}).get('text', '')
        print(f'=== {art}:{line} ===')
        print(repr(snippet[:200]))
