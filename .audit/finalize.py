"""Finalize calibration to match prior audit's grading scheme:
- unpinned-uses (zizmor error+high under --persona auditor) -> High
- secrets-outside-env (zizmor warning+high) -> Medium (carryover noise tier)
- artipacked (zizmor warning+low) -> Medium (already correct)
- All other classes -> per literal mapping.
"""

import json
import hashlib
import os
from collections import Counter

d = json.load(open('.audit/final.json'))
findings = d['findings']

for f in findings:
    if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
        f['severity'] = 'Medium'
        f.setdefault('calibrated_notes', []).append('secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)')

# Recount summary
sev = Counter(f['severity'] for f in findings)
new = [f for f in findings if f['delta'] == 'NEW']
unchanged = [f for f in findings if f['delta'] == 'UNCHANGED']
print('Recomputed severity totals:')
for s, n in sev.most_common():
    print(f'  {s}: {n}')

print(f'\nNEW after calibration:')
sev_new = Counter(f['severity'] for f in new)
for s, n in sev_new.most_common():
    print(f'  NEW {s}: {n}')
print()
sev_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
for f in sorted(new, key=lambda x: (sev_order[x['severity']], x['file'], x['line'])):
    print(f'  [{f["severity"]}] {f["short_rule"]:25s} {os.path.basename(f["file"])}:{f["line"]} step={f["step"]!r}')

# Save
json.dump({
    'findings': findings,
    'summary': {
        'total': len(findings),
        'crit': sev['Critical'],
        'high': sev['High'],
        'med': sev['Medium'],
        'low': sev['Low'],
        'new': len(new),
        'unchanged': len(unchanged),
        'new_by_sev': dict(sev_new),
    },
}, open('.audit/final2.json', 'w'), indent=2)
