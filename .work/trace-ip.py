import json
with open('/home/runner/work/aeon/aeon/.work/torlink/package-lock.json') as f:
    lock = json.load(f)
pkgs = lock.get('packages', {})
for path, info in pkgs.items():
    deps = info.get('dependencies', {})
    if 'ip' in deps:
        print(f'{path or "<root>"} depends on ip@{deps["ip"]}')
print('---')
for path, info in pkgs.items():
    if path.endswith('/ip') or path == 'node_modules/ip':
        print(f'{path}: version={info.get("version")}, resolved={info.get("resolved","")}')
