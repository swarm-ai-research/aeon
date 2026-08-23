import json
from collections import Counter

d = json.load(open('.audit/classified.json'))
c = d['current']
by_sev = Counter(f['severity'] for f in c)
print('total findings:', len(c))
print('by sev:', dict(by_sev))
print('all UNCHANGED:', all(f['status'] == 'UNCHANGED' for f in c))
files = {f['file'] for f in c}
print('files touched:', len(files))
for f in sorted(files):
    print(' ', f)
