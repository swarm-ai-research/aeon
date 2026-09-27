#!/usr/bin/env python3
import json, pprint
sarif = json.load(open('.audit/zizmor.sarif'))
results = sarif['runs'][0]['results']
print('total sarif results:', len(results))
pprint.pprint(results[0])
print('---')
pprint.pprint(results[10])
