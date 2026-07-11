"""Tally actionlint findings by shellcheck error code.

Reads .audit/actionlint.json and counts how many findings contain each of the
common shellcheck codes (SC2086, SC2046, SC2129, SC2153, SC2155, SC2034).
Also prints findings where SC2086 or SC2046 appear alongside a github.*
expression — those are the high-candidate injection patterns.
"""

import json
from collections import Counter
data = json.load(open('.audit/actionlint.json'))
codes = Counter()
for f in data:
    msg = f.get('message','')
    matched = False
    for code in ['SC2086','SC2046','SC2129','SC2153','SC2155','SC2034']:
        if code in msg:
            codes[code] += 1
            matched = True
            break
    if not matched:
        codes['other'] += 1
print('shellcheck codes:', dict(codes))
for f in data:
    msg = f.get('message','')
    if ('SC2086' in msg or 'SC2046' in msg) and 'github.' in msg.lower():
        print('HIGH-CANDIDATE:', f.get('filepath'), f.get('line'), msg[:120])
