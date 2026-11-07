import json
r = json.loads(open('.pr-tracker-tmp/result.json').read())
states = {}
for n in r['non_prefix']:
    states[n['state']] = states.get(n['state'], 0) + 1
print('non_prefix states:', states)
rv = [n for n in r['all_open'] if 'RuView' in n['repository']['nameWithOwner']][0]
print('RuView updatedAt:', rv['updatedAt'], 'comments:', rv['comments']['totalCount'], 'reviews:', rv['reviews'])
oc = [n for n in r['all_open'] if 'opencart' in n['repository']['nameWithOwner']][0]
print('opencart updatedAt:', oc['updatedAt'], 'comments:', oc['comments']['totalCount'], 'reviews:', oc['reviews'])
