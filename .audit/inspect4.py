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
        first = snippet.strip().splitlines()[0][:60] if snippet else ''
        print(f'{art}:{line}  step_ctx="{first}"')
