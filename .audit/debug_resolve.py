import re, os, json

_YAML_CACHE = {}
def _get_lines(path):
    if path not in _YAML_CACHE:
        try:
            _YAML_CACHE[path] = open(path).read().splitlines()
        except Exception:
            _YAML_CACHE[path] = []
    return _YAML_CACHE[path]

def resolve_step(file, line):
    lines = _get_lines(file)
    if not lines or line <= 0 or line > len(lines):
        return '(unknown)'
    for i in range(line-1, -1, -1):
        m = re.match(r'\s*-\s*name:\s*(.+?)\s*$', lines[i])
        if m:
            return m.group(1).strip('"\'').strip()
    return '(unknown)'

d = json.load(open('.audit/zizmor.sarif'))
seen = 0
for r in d['runs'][0]['results']:
    if r.get('ruleId') == 'zizmor/artipacked':
        locs = r.get('locations', [])
        if locs:
            uri = locs[0]['physicalLocation']['artifactLocation']['uri']
            line = locs[0]['physicalLocation']['region']['startLine']
            step = resolve_step(uri, line)
            print(f'{uri}:{line} -> step={step!r}')
            seen += 1
            if seen >= 5:
                break
