#!/usr/bin/env python3
import glob, re, os, json
os.chdir("/home/runner/work/aeon/aeon")
with open("skills.json") as f:
    sj = json.load(f)
json_cat = {s["slug"]: s["category"] for s in sj["skills"]}

uncat = []
for p in sorted(glob.glob("skills/*/SKILL.md")):
    slug = p.split("/")[1]
    if slug in json_cat:
        continue
    with open(p) as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    tags = ""
    if m:
        tm = re.search(r"^tags:\s*(\[[^\]]*\])", m.group(1), re.MULTILINE)
        if tm:
            tags = tm.group(1)
    uncat.append((slug, tags))

print(f"total not in skills.json: {len(uncat)}")
for s, t in uncat:
    print(f"  {s:40s} tags={t}")
