import re, os

_YAML_CACHE = {}
def _resolve_path(path):
    if os.path.exists(path):
        return path
    for prefix in ('.github/workflows/', '.github/actions/'):
        candidate = prefix + path
        if os.path.exists(candidate):
            return candidate
    return path

def _get_lines(path):
    real = _resolve_path(path)
    if real not in _YAML_CACHE:
        try:
            _YAML_CACHE[real] = open(real).read().splitlines()
        except Exception:
            _YAML_CACHE[real] = []
    return _YAML_CACHE[real]

def resolve_step(file, line):
    lines = _get_lines(file)
    if not lines or line <= 0 or line > len(lines):
        return '(unknown)'
    for i in range(line-1, -1, -1):
        m = re.match(r'\s*-\s*name:\s*(.+?)\s*$', lines[i])
        if m:
            return m.group(1).strip('"\'').strip()
    return '(unknown)'

# Test with aeon.yml:98
print('aeon.yml:98 ->', resolve_step('aeon.yml', 98))
print('aeon.yml:602 ->', resolve_step('aeon.yml', 602))
