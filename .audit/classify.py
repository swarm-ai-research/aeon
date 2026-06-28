import json
import hashlib
import os
import re
from collections import Counter, defaultdict

from lib import our_severity

findings = json.load(open('.audit/parsed.json'))

for f in findings:
    f['severity'] = our_severity(f)
    short_rule = f['rule_id'].split('/')[-1]
    f['short_rule'] = short_rule
    # Build fingerprint: rule_id|file|step_or_snippet-key
    snip_key = re.sub(r'\s+', ' ', f['snippet'])[:60]
    file_short = os.path.basename(f['file'])
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    f['fingerprint'] = hashlib.sha256(fp_src.encode()).hexdigest()[:16]

print(f'Severity distribution:')
for s, n in Counter(f['severity'] for f in findings).most_common():
    print(f'  {n:4d}  {s}')

print(f'\nCritical findings:')
for f in [x for x in findings if x['severity'] == 'Critical']:
    print(f"  [{f['rule_id']}] {os.path.basename(f['file'])}:{f['line']} — {f['message'][:80]}")

print(f'\nHigh findings (first 20):')
for f in [x for x in findings if x['severity'] == 'High'][:20]:
    print(f"  [{f['short_rule']}] {os.path.basename(f['file'])}:{f['line']} — conf={f['confidence']} level={f['level']}")

# Save with severity + fingerprint
json.dump(findings, open('.audit/classified.json', 'w'), indent=2)
