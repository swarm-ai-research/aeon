#!/usr/bin/env python3
import json, os
from collections import Counter
os.chdir("/home/runner/work/aeon/aeon")
with open("skills.json") as f:
    sj = json.load(f)
cats = Counter(s["category"] for s in sj["skills"])
print(cats)
print("JSON categories key:", sj.get("categories", {}).keys())
