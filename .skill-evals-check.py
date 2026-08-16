import os, glob, json, re, time

BASE = "/home/runner/work/aeon/aeon"
os.chdir(BASE)

skills_patterns = {
    "heartbeat": "memory/logs/*.md",
    "repo-pulse": "articles/repo-pulse-*.md",
    "changelog": "articles/changelog-*.md",
    "push-recap": "articles/push-recap-*.md",
    "fork-fleet": "articles/fork-fleet-*.md",
    "cost-report": "articles/cost-report-*.md",
    "repo-article": "articles/repo-article-*.md",
    "repo-actions": "articles/repo-actions-*.md",
    "deep-research": "articles/deep-research-*.md",
    "hn-digest": "articles/hn-digest-*.md",
    "rss-digest": "articles/rss-digest-*.md",
    "polymarket": "articles/polymarket-*.md",
    "token-alert": "articles/token-alert-*.md",
    "skill-health": "memory/skill-health/last-report.json",
    "swarm-safety-eval": "articles/swarm-safety-eval-*.md",
}

now = time.time()
results = {}
for skill, pattern in skills_patterns.items():
    files = sorted(glob.glob(pattern), reverse=True)
    if not files:
        results[skill] = {"status": "NO_OUTPUT", "file": None, "size": 0, "age_days": None}
        continue
    latest = files[0]
    size = os.path.getsize(latest)
    mtime = os.path.getmtime(latest)
    age_days = (now - mtime) / 86400
    results[skill] = {"file": latest, "size": size, "age_days": round(age_days, 1)}

print(json.dumps(results, indent=2))
