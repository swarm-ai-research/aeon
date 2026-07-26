#!/usr/bin/env python3
import hashlib, os, re, glob, subprocess, json

root = "/home/runner/work/aeon/aeon"
os.chdir(root)

h = hashlib.sha1()

# sha1sum aeon.yml + skills.json
for f in ["aeon.yml", "skills.json"]:
    with open(f, "rb") as fp:
        h1 = hashlib.sha1(fp.read()).hexdigest()
        h.update(f"{h1}  {f}\n".encode())

# Per-skill: frontmatter + edge-lines + memory-refs
frontmatter_re = re.compile(r'^---$')
edge_re = re.compile(r'^(depends_on:|- skill:|consume:|parallel:|trigger:)')
mem_re = re.compile(r'memory/(topics|state)/[a-zA-Z0-9_.-]+')

for path in sorted(glob.glob("skills/*/SKILL.md")):
    with open(path, "r", encoding="utf-8", errors="replace") as fp:
        lines = fp.readlines()
    n = 0
    for line in lines:
        if frontmatter_re.match(line.rstrip("\n")):
            n += 1
            continue
        if n == 1:
            h.update(f"{path}: {line.rstrip(chr(10))}\n".encode())
    for line in lines:
        if edge_re.match(line):
            h.update(line.encode())
    mems = sorted(set(m.group(0) for m in mem_re.finditer("".join(lines))))
    for m in mems:
        h.update((m+"\n").encode())

print(h.hexdigest())
