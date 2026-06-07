import json
data = json.load(open('.audit/actionlint.json'))
for f in data:
    msg = f.get('message','')
    if 'SC2086' in msg:
        print(f.get('filepath'), ':', f.get('line'), msg[:200])
