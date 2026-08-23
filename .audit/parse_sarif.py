#!/usr/bin/env python3
"""Parse zizmor SARIF into normalized findings."""
import json
import hashlib

sarif = json.load(open('.audit/zizmor.sarif'))
results = sarif['runs'][0]['results']


def sev_map(zsev, zconf):
    zsev = (zsev or '').lower()
    zconf = (zconf or '').lower()
    if zsev == 'high' and zconf == 'high':
        return 'Critical'
    if zsev == 'high':
        return 'High'
    if zsev == 'medium' and zconf == 'high':
        return 'High'
    if zsev == 'medium':
        return 'Medium'
    return 'Low'


def get_step_from_route(logical):
    if not logical:
        return ''
    props = logical[0].get('properties', {})
    sym = props.get('symbolic', {})
    route = sym.get('route', {}).get('route', [])
    parts = []
    for r in route:
        if 'Key' in r:
            parts.append(str(r['Key']))
        elif 'Index' in r:
            parts.append(f"[{r['Index']}]")
    return '.'.join(parts)


findings = []
for r in results:
    ruleid = r.get('ruleId', 'unknown')
    level = r.get('level', 'note')
    props = r.get('properties', {})
    zsev = props.get('zizmor/severity', '')
    zconf = props.get('zizmor/confidence', '')
    persona = props.get('zizmor/persona', '')
    text = r.get('message', {}).get('text', '')
    loc = r['locations'][0]
    pl = loc.get('physicalLocation', {})
    uri = pl.get('artifactLocation', {}).get('uri', '')
    # zizmor emits URIs relative to the input dir root
    if not uri.startswith('.github/'):
        # workflow files came in from .github/workflows/
        uri = f'.github/workflows/{uri}'
    region = pl.get('region', {})
    line = region.get('startLine', 0)
    snippet_text = ''
    if 'snippet' in region and isinstance(region['snippet'], dict):
        snippet_text = region['snippet'].get('text', '')
    route_step = get_step_from_route(loc.get('logicalLocations', []))
    sev = sev_map(zsev, zconf)
    # Fingerprint: rule + file + route path (stable across line drift)
    fp_input = f"{ruleid}|{uri}|{route_step}"
    fp = hashlib.sha256(fp_input.encode()).hexdigest()[:16]
    findings.append({
        'fingerprint': fp,
        'severity': sev,
        'rule_id': ruleid,
        'file': uri,
        'line': line,
        'step': route_step,
        'pattern': snippet_text[:200],
        'source': 'zizmor',
        'zsev': zsev,
        'zconf': zconf,
        'persona': persona,
        'level': level,
        'message': text[:600],
    })

by_sev = {}
by_rule = {}
for f in findings:
    by_sev[f['severity']] = by_sev.get(f['severity'], 0) + 1
    by_rule[f['rule_id']] = by_rule.get(f['rule_id'], 0) + 1

print(f"zizmor findings: {len(findings)}")
print(f"by severity: {by_sev}")
print("by rule:")
for k, v in sorted(by_rule.items(), key=lambda x: -x[1]):
    print(f"  {v:3d} {k}")

open('.audit/parsed.json', 'w').write(json.dumps(findings, indent=2))
