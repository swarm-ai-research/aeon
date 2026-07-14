import json
from collections import Counter
data = json.load(open('.audit/actionlint.json'))
codes = Counter()
_SC_CODES = ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']
for f in data:
    msg = f.get('message', '')
    codes[next((c for c in _SC_CODES if c in msg), 'other')] += 1
print('shellcheck codes:', dict(codes))
for f in data:
    msg = f.get('message','')
    if ('SC2086' in msg or 'SC2046' in msg) and 'github.' in msg.lower():
        print('HIGH-CANDIDATE:', f.get('filepath'), f.get('line'), msg[:120])
