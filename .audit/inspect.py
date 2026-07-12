import json
d = json.load(open('.audit/zizmor.sarif'))
r = d['runs'][0]['results']
seen = set()
for x in r[:30]:
    uri = x.get('locations',[{}])[0].get('physicalLocation',{}).get('artifactLocation',{}).get('uri')
    seen.add(uri)
print('unique uris in first 30:', seen)
print('total unique uris:', len({x['locations'][0]['physicalLocation']['artifactLocation']['uri'] for x in r if x.get('locations')}))
print('driver:', d['runs'][0]['tool']['driver'].get('name'), d['runs'][0]['tool']['driver'].get('version'))
print('originalUri:', d['runs'][0].get('originalUriBaseIds'))
# Print rule ids observed with counts
from collections import Counter
c = Counter(x.get('ruleId') for x in r)
print('rule counts:')
for k,v in c.most_common():
    print(f'  {v:4d}  {k}')
