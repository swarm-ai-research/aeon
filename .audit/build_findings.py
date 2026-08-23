#!/usr/bin/env python3
"""Build the unified current-run findings set with prior-compatible fingerprints."""
import glob
import hashlib
import json
import os
import re

# --- Load zizmor SARIF ---
sarif = json.load(open('.audit/zizmor.sarif'))
z_results = sarif['runs'][0]['results']

# --- Load actionlint JSON ---
al_results = json.load(open('.audit/actionlint.json'))


def sarif_severity(level, zsev, zconf):
    """Map SARIF level → our severity per skill."""
    zsev = (zsev or '').lower()
    zconf = (zconf or '').lower()
    if level == 'error' and zconf == 'high':
        return 'Critical'
    if level == 'error':
        return 'High'
    if level == 'warning' and zconf == 'high':
        return 'High'
    if level == 'warning':
        return 'Medium'
    return 'Low'


def build_step_map(file_path):
    """Build 1-indexed line -> step name mapping by walking file, tracking most recent `- name:`."""
    try:
        lines = open(file_path).readlines()
    except FileNotFoundError:
        return {}
    step_map = {}
    current = '(unknown)'
    for i, line in enumerate(lines, 1):
        m = re.match(r"""^\s*-\s*name:\s*['"]?(.+?)['"]?\s*(#.*)?$""", line)
        if m:
            current = m.group(1).strip()
        step_map[i] = current
    return step_map


def resolve_uri(uri):
    """zizmor emits URIs as basenames like `aeon.yml`; resolve into full workflow path.

    Prefers `.github/workflows/<uri>` because the repo has a top-level
    `aeon.yml` (skill schedule) that collides with the workflow filename.
    """
    if not uri:
        return ''
    if uri.startswith('.github/'):
        return uri
    cand = os.path.join('.github/workflows', uri)
    if os.path.exists(cand):
        return cand
    # composite actions live under .github/actions/*/action.y[a]ml
    cand2 = os.path.join('.github/actions', uri)
    if os.path.exists(cand2):
        return cand2
    return uri  # last-resort fall back to as-is


def fp12(rule, file, step):
    """Prior fingerprint scheme: sha256("<rule>|<file>|<step-with-spaces>")[:12]."""
    return hashlib.sha256(f"{rule}|{file}|{step}".encode()).hexdigest()[:12]


# --- Build step maps for all files referenced ---
files_referenced = set()
for r in z_results:
    loc = r['locations'][0]['physicalLocation']['artifactLocation']['uri']
    files_referenced.add(resolve_uri(loc))
for e in al_results:
    if 'filepath' in e:
        files_referenced.add(e['filepath'])
step_maps = {f: build_step_map(f) for f in files_referenced}


findings = []

# --- Process zizmor findings ---
for r in z_results:
    rule_id = r.get('ruleId', 'unknown')
    level = r.get('level', 'note')
    props = r.get('properties', {})
    zsev = props.get('zizmor/severity', '')
    zconf = props.get('zizmor/confidence', '')
    persona = props.get('zizmor/persona', '')
    text = r.get('message', {}).get('text', '')
    loc = r['locations'][0]
    pl = loc.get('physicalLocation', {})
    raw_uri = pl.get('artifactLocation', {}).get('uri', '')
    file = resolve_uri(raw_uri)
    region = pl.get('region', {})
    line = region.get('startLine', 0)
    snippet = ''
    if 'snippet' in region and isinstance(region['snippet'], dict):
        snippet = region['snippet'].get('text', '')
    step = step_maps.get(file, {}).get(line, '(unknown)')
    sev = sarif_severity(level, zsev, zconf)
    findings.append({
        'fingerprint': fp12(rule_id, file, step),
        'severity': sev,
        'rule_id': rule_id,
        'file': file,
        'line': line,
        'step': step,
        'pattern': snippet[:200],
        'source': 'zizmor',
        'zsev': zsev,
        'zconf': zconf,
        'persona': persona,
        'level': level,
        'message': text[:600],
    })

# --- Process actionlint findings ---
def al_severity(kind, msg):
    """Per skill: actionlint → Medium, unless SC2086/SC2046 over ${{ github.* }} → High."""
    if kind == 'shellcheck':
        m = re.match(r'shellcheck reported issue in this script:\s*(SC\d+):', msg)
        code = m.group(1) if m else 'shellcheck'
        # Escalate injection-relevant codes over github.* interpolation to High
        if code in ('SC2086', 'SC2046') and '${{ github' in msg:
            return 'High', code
        return 'Medium', code
    return 'Medium', kind


for e in al_results:
    fp = e.get('filepath', '')
    line = e.get('line', 0)
    kind = e.get('kind', 'unknown')
    msg = e.get('message', '')
    sev, code = al_severity(kind, msg)
    rule_id = f'actionlint/{code}' if code else f'actionlint/{kind}'
    step = step_maps.get(fp, {}).get(line, '(unknown)')
    findings.append({
        'fingerprint': fp12(rule_id, fp, step),
        'severity': sev,
        'rule_id': rule_id,
        'file': fp,
        'line': line,
        'step': step,
        'pattern': msg[:200],
        'source': 'actionlint',
        'zsev': '',
        'zconf': '',
        'persona': '',
        'level': '',
        'message': msg[:600],
    })

# --- Hand-rolled findings ---
hr = json.load(open('.audit/handrolled.json'))
for f in hr:
    step = step_maps.get(f['file'], {}).get(f['line'], f.get('step', '(unknown)'))
    findings.append({
        'fingerprint': fp12(f['rule_id'], f['file'], step),
        'severity': f['severity'],
        'rule_id': f['rule_id'],
        'file': f['file'],
        'line': f['line'],
        'step': step,
        'pattern': f['pattern'][:200],
        'source': 'hand-rolled',
        'zsev': '',
        'zconf': '',
        'persona': '',
        'level': '',
        'message': f['pattern'][:600],
    })

# --- De-duplicate fingerprints (multiple SARIF hits on same rule+file+step collapse) ---
seen = {}
for f in findings:
    fp = f['fingerprint']
    if fp not in seen:
        seen[fp] = f
    else:
        # Prefer the first, but if the new one has a smaller line number keep it for locality
        if f['line'] and (not seen[fp]['line'] or f['line'] < seen[fp]['line']):
            # keep earlier line for readability
            f2 = dict(seen[fp])
            f2['line'] = f['line']
            f2['pattern'] = f['pattern'] or f2['pattern']
            seen[fp] = f2

deduped = list(seen.values())

from collections import Counter
by_sev = Counter(f['severity'] for f in deduped)
by_rule = Counter(f['rule_id'] for f in deduped)
print(f"total pre-dedup: {len(findings)}   post-dedup: {len(deduped)}")
print(f"by severity: {dict(by_sev)}")
print("by rule:")
for k, v in sorted(by_rule.items(), key=lambda x: -x[1]):
    print(f"  {v:3d} {k}")

open('.audit/current.json', 'w').write(json.dumps(deduped, indent=2))
