import yaml, json
text = open('aeon.yml').read()
doc = yaml.safe_load(text)
skills_section = doc.get('skills', {})
enabled = {k: v for k, v in skills_section.items() if isinstance(v, dict) and v.get('enabled') is True}
print(f'enabled_count={len(enabled)}')
for k in sorted(enabled):
    print('  ', k)
