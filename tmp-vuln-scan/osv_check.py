import json
import urllib.request

PKGS = [
    ("cryptography", "50.0.2"),
    ("cryptography", "48.0.1"),
    ("cffi", "2.0.0"),
    ("pycparser", "2.23"),
    ("typing-extensions", "4.16.0"),
    ("yara-x", "1.21.0"),
]

for name, ver in PKGS:
    body = json.dumps({"version": ver, "package": {"name": name, "ecosystem": "PyPI"}}).encode()
    req = urllib.request.Request(
        "https://api.osv.dev/v1/query",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            d = json.load(resp)
    except Exception as e:
        print(f"ERR {name} {ver}: {e}")
        continue
    vulns = d.get("vulns", [])
    print(f"=== {name} {ver} === {len(vulns)} vulns")
    for v in vulns:
        severity = ""
        for s in v.get("severity", []):
            severity = s.get("score", "")
            break
        print(f"  {v.get('id')} [{severity}] {v.get('summary','')[:150]}")
