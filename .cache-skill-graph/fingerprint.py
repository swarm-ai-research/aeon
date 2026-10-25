#!/usr/bin/env python3
"""Compute input fingerprint for skill-graph."""
import glob
import hashlib
import re
import os

os.chdir("/home/runner/work/aeon/aeon")

h = hashlib.sha1()

# aeon.yml + skills.json
for p in ["aeon.yml", "skills.json"]:
    with open(p, "rb") as f:
        d = f.read()
    h.update(f"{hashlib.sha1(d).hexdigest()}  {p}\n".encode())

acc = []
for f in sorted(glob.glob("skills/*/SKILL.md")):
    with open(f, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    # Frontmatter (lines between first two '---')
    lines = text.split("\n")
    n = 0
    for line in lines:
        if line.strip() == "---":
            n += 1
            continue
        if n == 1:
            acc.append(f"{f}: {line}")

    # depends_on / - skill: / consume: / parallel: / trigger:
    for line in lines:
        if re.match(r"^(depends_on:|- skill:|consume:|parallel:|trigger:)", line):
            acc.append(line)

    # memory/(topics|state)/X refs
    refs = set(re.findall(r"memory/(?:topics|state)/[a-zA-Z0-9_.-]+", text))
    acc.extend(sorted(refs))

skills_hash = hashlib.sha1("\n".join(acc).encode()).hexdigest()
h.update(f"{skills_hash}  -\n".encode())
print(h.hexdigest())
