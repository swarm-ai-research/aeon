#!/usr/bin/env python3
"""Classify current findings vs prior audit's fingerprints."""
import json
import re
import subprocess

# Prior report source: PR #24 branch — the last audit that wrote a report is not
# on main, but its report + fingerprint trailer lives on
# fix/workflow-security-audit-2026-08-09. Fall back to no-prior if the fetch fails.
PRIOR_BRANCH = 'fix/workflow-security-audit-2026-08-09'
PRIOR_PATH = 'articles/workflow-security-audit-2026-08-09.md'
PRIOR_DATE = '2026-08-09'

prior_fps = {}  # fp -> {severity, status, rule, file, step}

try:
    r = subprocess.run(
        ['gh', 'api',
         f'repos/swarm-ai-research/aeon/contents/{PRIOR_PATH}?ref={PRIOR_BRANCH}',
         '--jq', '.content'],
        capture_output=True, text=True, check=True,
    )
    import base64
    text = base64.b64decode(r.stdout).decode('utf-8', errors='ignore')
    m = re.search(r'workflow-security-audit-fingerprints\s*\n(.*?)(?:\n-->|$)', text, re.DOTALL)
    if m:
        for ln in m.group(1).strip().split('\n'):
            ln = ln.strip()
            if not ln or ln.startswith('#'):
                continue
            parts = ln.split()
            fp = parts[0]
            attrs = {}
            for kv in parts[1:]:
                if '=' in kv:
                    k, v = kv.split('=', 1)
                    attrs[k] = v
            prior_fps[fp] = attrs
    print(f"loaded {len(prior_fps)} prior fingerprints from {PRIOR_BRANCH}:{PRIOR_PATH}")
except Exception as e:
    print(f"WARN: could not load prior report: {e}")

current = json.load(open('.audit/current.json'))
current_fps = {f['fingerprint']: f for f in current}

# Classify
for f in current:
    fp = f['fingerprint']
    if fp not in prior_fps:
        f['status'] = 'NEW'
    else:
        prior_status = prior_fps[fp].get('status', 'manual')
        if prior_status in ('auto-fixed', 'resolved'):
            f['status'] = 'REINTRODUCED'
        else:
            f['status'] = 'UNCHANGED'

# RESOLVED = prior fp absent from current
resolved = []
for fp, attrs in prior_fps.items():
    if fp not in current_fps:
        resolved.append({'fingerprint': fp, **attrs})

from collections import Counter
by_status_sev = Counter((f['status'], f['severity']) for f in current)
print("current findings by (status, severity):")
for k, v in sorted(by_status_sev.items()):
    print(f"  {k}: {v}")
print(f"resolved (prior fp gone from current): {len(resolved)}")

# Save results
open('.audit/classified.json', 'w').write(json.dumps({
    'current': current,
    'resolved': resolved,
    'prior_date': PRIOR_DATE,
    'prior_source': f'{PRIOR_BRANCH}:{PRIOR_PATH}',
    'prior_count': len(prior_fps),
}, indent=2))
