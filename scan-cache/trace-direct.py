"""Categorize each OSV-flagged package as direct vs transitive."""
import json

with open('/home/runner/work/aeon/aeon/scan-cache/out/osv-clean.json') as f:
    data = json.load(f)

# Collect package.json direct deps across the workspace
import os, glob
direct = set()
package_files = []
for root, dirs, files in os.walk('/home/runner/work/aeon/aeon/scan-cache/repo/eve'):
    if 'node_modules' in root.split(os.sep): continue
    if '.git' in root.split(os.sep): continue
    for f in files:
        if f == 'package.json':
            package_files.append(os.path.join(root, f))

direct_in_pkg = {}
for pf in package_files:
    try:
        with open(pf) as f:
            d = json.load(f)
        for k in ('dependencies','devDependencies','peerDependencies'):
            for name, ver in (d.get(k) or {}).items():
                direct.add(name)
                direct_in_pkg.setdefault(name, []).append((pf.replace('/home/runner/work/aeon/aeon/scan-cache/repo/eve/',''), k, ver))
    except Exception:
        pass

# Distinct vulnerable packages
vuln_packages = set()
for src in data.get('results', []):
    for pkg in src.get('packages', []):
        if pkg.get('vulnerabilities'):
            vuln_packages.add((pkg['package']['name'], pkg['package']['version']))

print(f"Workspace package.json files: {len(package_files)}")
print(f"Distinct direct deps: {len(direct)}")
print(f"Distinct vulnerable packages: {len(vuln_packages)}\n")

print("=== Vulnerable packages by direct/transitive status ===")
for (name, ver) in sorted(vuln_packages):
    if name in direct:
        sites = direct_in_pkg[name]
        print(f"  [DIRECT] {name}@{ver}  -> {len(sites)} sites")
        for s in sites[:5]:
            print(f"      {s[0]} ({s[1]}: {s[2]})")
    else:
        print(f"  [transitive] {name}@{ver}")
