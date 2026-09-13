#!/usr/bin/env python3
"""Compute skill-graph input fingerprint per SKILL.md step 1."""
import hashlib
import glob
import re
import os
import sys

ROOT = "/home/runner/work/aeon/aeon"
os.chdir(ROOT)

buf = []

# SHA1 of aeon.yml + skills.json
for path in ["aeon.yml", "skills.json"]:
    with open(path, "rb") as fh:
        h = hashlib.sha1(fh.read()).hexdigest()
        buf.append(f"{h}  {path}\n")

# For each SKILL.md: frontmatter lines, edge markers, memory refs
for f in sorted(glob.glob("skills/*/SKILL.md")):
    try:
        with open(f, encoding="utf-8") as fh:
            lines = fh.readlines()
    except Exception:
        continue
    # frontmatter only (between first pair of ---)
    in_fm = False
    fm_seen = 0
    for ln in lines:
        if ln.rstrip() == "---":
            fm_seen += 1
            if fm_seen == 1:
                in_fm = True
                continue
            if fm_seen == 2:
                in_fm = False
                break
        if in_fm:
            buf.append(f"{f}: {ln.rstrip()}\n")
    # edge markers
    for ln in lines:
        if re.match(r"^(depends_on:|- skill:|consume:|parallel:|trigger:)", ln.strip()):
            buf.append(ln)
    # memory refs (sorted unique)
    text = "".join(lines)
    refs = sorted(set(re.findall(r"memory/(?:topics|state)/[a-zA-Z0-9_.-]+", text)))
    for r in refs:
        buf.append(r + "\n")

payload = "".join(buf).encode("utf-8")
print(hashlib.sha1(payload).hexdigest())
