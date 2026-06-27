"""For each vulnerable package, extract minimum fixed version from OSV affected.ranges."""
import json
from collections import defaultdict

with open('/home/runner/work/aeon/aeon/scan-cache/out/osv-clean.json') as f:
    data = json.load(f)

def severity_label(score_str):
    if not score_str:
        return "?"
    # CVSS:3.x or 4.0 — pull the base score from the vector if present; otherwise tier by AV/C/I/A
    return score_str[:24]

# Direct deps from prior trace
direct = {
    '@opentelemetry/core', 'nuxt', 'postcss', 'vite'
}

pkg_findings = defaultdict(list)  # name@ver -> list of (vid, summary, severity, fixed_versions_set)
for src in data.get('results', []):
    for pkg in src.get('packages', []):
        vulns = pkg.get('vulnerabilities', [])
        if not vulns: continue
        name = pkg['package']['name']
        ver = pkg['package']['version']
        for v in vulns:
            vid = v.get('id','?')
            summary = v.get('summary') or v.get('details','')[:120]
            sev_score = ''
            for s in v.get('severity',[]):
                sev_score = s.get('score','')
                break
            fixed = set()
            for a in v.get('affected',[]):
                if a.get('package',{}).get('name') != name: continue
                for r in a.get('ranges',[]):
                    for ev in r.get('events',[]):
                        if 'fixed' in ev:
                            fixed.add(ev['fixed'])
                        if 'last_affected' in ev:
                            fixed.add(f"after {ev['last_affected']}")
            pkg_findings[f"{name}@{ver}"].append((vid, sev_score, summary, sorted(fixed)))

# Print summarized table
print(f"{'package':40s}  {'vid':30s}  {'fix':20s}  summary")
print("-"*180)
for key in sorted(pkg_findings):
    name = key.split('@')[0]
    mark = "DIRECT" if name in direct else ""
    for (vid, sev, summary, fixed) in pkg_findings[key]:
        fix_str = ",".join(fixed[:2]) if fixed else "—"
        print(f"{key:40s}  {vid:30s}  {fix_str:20s}  [{mark:6s}] {summary[:90]}")
