#!/usr/bin/env python3
"""Extract all zizmor template-injection findings with confidence and severity."""
import json
data = json.load(open('.audit/zizmor.sarif'))
results = data['runs'][0]['results']
for r in results:
    if r.get('ruleId') != 'zizmor/template-injection':
        continue
    props = r.get('properties', {})
    conf = ''
    for k, v in props.items():
        if 'confidence' in k.lower():
            conf = v
            break
    locs = r.get('locations', [])
    if not locs:
        continue
    pl = locs[0].get('physicalLocation', {})
    file = pl.get('artifactLocation', {}).get('uri', '')
    line = pl.get('region', {}).get('startLine', 0)
    end_line = pl.get('region', {}).get('endLine', 0)
    msg = r.get('message', {}).get('text', '')
    print(f'{r.get("level"):8s} conf={conf:8s} {file}:{line}-{end_line}  {msg[:110]}')
