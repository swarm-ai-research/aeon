import json, sys

with open('/home/runner/work/aeon/aeon/scan-cache/out/osv.json') as f:
    content = f.read()

idx = content.find('\n{')
if idx == -1:
    idx = content.find('{')
else:
    idx += 1

data = json.loads(content[idx:])

with open('/home/runner/work/aeon/aeon/scan-cache/out/osv-clean.json','w') as f:
    json.dump(data, f, indent=2)

total_vulns = 0
pkgs_with_vulns = 0
rows = []
for src in data.get('results', []):
    for pkg in src.get('packages', []):
        vulns = pkg.get('vulnerabilities', [])
        if vulns:
            pkgs_with_vulns += 1
            total_vulns += len(vulns)
            name = pkg['package']['name']
            ver = pkg['package']['version']
            for v in vulns:
                vid = v.get('id', '?')
                summary = v.get('summary') or v.get('details', '')[:80] or '(no summary)'
                sev = ''
                for s in v.get('severity', []):
                    sev = s.get('score', '')
                    break
                grp = pkg.get('groups', [])
                aliases = v.get('aliases', [])
                rows.append((name, ver, vid, aliases, sev, summary))

rows.sort()
for r in rows:
    print(f"{r[0]}@{r[1]} | {r[2]} | aliases={r[3]} | {r[4]} | {r[5]}")
print(f"\n--- pkgs_with_vulns={pkgs_with_vulns} total_advisories={total_vulns}")
