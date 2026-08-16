import os, glob, json, re, time

BASE = "/home/runner/work/aeon/aeon"
os.chdir(BASE)

evals = json.load(open("skills/skill-evals/evals.json"))

skills_to_check = {
    "heartbeat": "memory/logs/2026-08-16.md",
    "skill-health": "memory/skill-health/last-report.json",
}

skill_health_scores = {}
for f in glob.glob("memory/skill-health/*.json"):
    skill = os.path.basename(f).replace(".json","")
    if skill == "last-report":
        continue
    try:
        d = json.load(open(f))
        skill_health_scores[skill] = d.get("avg_score")
    except:
        pass

print("=== SKILL HEALTH SCORES ===")
for k,v in skill_health_scores.items():
    print(f"  {k}: {v}")

now = time.time()
print()
print("=== ASSERTIONS ===")
for skill, filepath in skills_to_check.items():
    spec = evals["skills"][skill]
    if not os.path.exists(filepath):
        print(f"{skill}: NO_OUTPUT (file gone)")
        continue

    content = open(filepath).read()
    size = os.path.getsize(filepath)
    mtime = os.path.getmtime(filepath)
    age_days = (now - mtime) / 86400
    word_count = len(content.split())

    issues = []

    # Empty check
    if size == 0:
        issues.append("FAIL:empty_file")

    # Word count
    min_words = spec.get("min_words", 0)
    if word_count < min_words:
        issues.append(f"FAIL:word_count ({word_count} < {min_words})")

    # Required patterns
    for pat in spec.get("required_patterns", []):
        if not re.search(pat, content, re.IGNORECASE):
            issues.append(f"FAIL:missing_pattern:{pat}")

    # Forbidden patterns
    for pat in spec.get("forbidden_patterns", []):
        if re.search(pat, content):
            issues.append(f"FAIL:forbidden_pattern:{pat}")

    # Numeric checks
    for nc in spec.get("numeric_checks", []):
        match = re.search(nc["pattern"], content)
        if not match:
            if nc.get("skip_if_not_found"):
                continue
            issues.append(f"WARN:numeric_missing:{nc['label']}")
        else:
            val = float(match.group(1))
            if val < nc["min"] or val > nc["max"]:
                issues.append(f"FAIL:numeric_oob:{nc['label']} ({val})")

    # Quality
    qscore = skill_health_scores.get(skill)
    quality_note = ""
    if qscore is None:
        quality_note = "quality=unknown"
    elif qscore < 2.5:
        issues.append(f"QUALITY_DEGRADED:quality_score:{qscore}")
        quality_note = f"quality={qscore} (DEGRADED)"
    elif qscore < 3.5:
        quality_note = f"quality={qscore} (note: below 3.5)"
    else:
        quality_note = f"quality={qscore}"

    if issues:
        print(f"{skill}: ISSUES={issues} words={word_count} age={age_days:.1f}d {quality_note}")
    else:
        print(f"{skill}: PASS words={word_count} age={age_days:.1f}d {quality_note}")
