import json
with open('.audit/zizmor.sarif') as f:
    sarif = json.load(f)

def route_key(result):
    """Extract logical route from codeFlows (job.step index path)."""
    cfs = result.get('codeFlows') or []
    if not cfs:
        return ""
    tfs = cfs[0].get('threadFlows') or []
    if not tfs:
        return ""
    locs = tfs[0].get('locations') or []
    if not locs:
        return ""
    logs = locs[0].get('location', {}).get('logicalLocations') or []
    if not logs:
        return ""
    sym = logs[0].get('properties', {}).get('symbolic', {})
    route = sym.get('route', {}).get('route') or []
    parts = []
    for r in route:
        if 'Key' in r:
            parts.append(str(r['Key']))
        elif 'Index' in r:
            parts.append(f"[{r['Index']}]")
    return ".".join(parts)

for r in sarif['runs'][0]['results']:
    if r.get('ruleId') == 'zizmor/unpinned-uses':
        loc = (r.get('locations') or [{}])[0]
        pl = loc.get('physicalLocation') or {}
        art = (pl.get('artifactLocation') or {}).get('uri', '')
        line = (pl.get('region') or {}).get('startLine')
        print(f'{art}:{line}  route={route_key(r)}')
