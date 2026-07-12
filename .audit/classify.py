#!/usr/bin/env python3
"""Classify findings as NEW / REINTRODUCED / UNCHANGED / RESOLVED against prior report."""
import json, pathlib, re, glob

FIND = json.loads(pathlib.Path(".audit/parsed.json").read_text())

# Only consider prior reports that live on main (per SKILL step 4).
PRIOR_PATTERN = "articles/workflow-security-audit-*.md"
priors = sorted(glob.glob(PRIOR_PATTERN))
PRIOR = priors[-1] if priors else None

prior_fps = {}
if PRIOR:
    text = pathlib.Path(PRIOR).read_text()
    m = re.search(r'workflow-security-audit-fingerprints(.*?)-->', text, re.DOTALL)
    if m:
        for ln in m.group(1).strip().splitlines():
            parts = ln.split()
            if not parts:
                continue
            fp = parts[0]
            kv = dict(p.split("=",1) for p in parts[1:] if "=" in p)
            prior_fps[fp] = kv

for x in FIND:
    fp = x["fingerprint"]
    prior = prior_fps.get(fp)
    if prior is None:
        x["classification"] = "NEW"
    else:
        prior_status = prior.get("status","")
        if prior_status in ("auto-fixed","resolved","fixed"):
            x["classification"] = "REINTRODUCED"
        else:
            x["classification"] = "UNCHANGED"

resolved = []
current_fps = {x["fingerprint"] for x in FIND}
for fp, kv in prior_fps.items():
    if fp not in current_fps:
        resolved.append({"fingerprint": fp, **kv, "classification":"RESOLVED"})

out = {"prior": PRIOR, "findings": FIND, "resolved": resolved}
pathlib.Path(".audit/classified.json").write_text(json.dumps(out, indent=2))
counts = {"NEW":0,"REINTRODUCED":0,"UNCHANGED":0,"RESOLVED":len(resolved)}
sev_counts = {"NEW":{},"REINTRODUCED":{},"UNCHANGED":{}}
for x in FIND:
    counts[x["classification"]] += 1
    d = sev_counts[x["classification"]]
    d[x["severity"]] = d.get(x["severity"],0) + 1
print("prior report:", PRIOR)
print("counts:", counts)
print("severity by classification:", sev_counts)
