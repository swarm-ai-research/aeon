#!/usr/bin/env python3
"""Categorize PRs and compute canonical hash."""
import json, hashlib, pathlib
from datetime import datetime, timezone

data = json.loads(pathlib.Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/prs.json").read_text())
nodes = data["data"]["search"]["nodes"]

# OR filter: branch prefix OR bot email in known list
BRANCH_PREFIXES = ("ai/", "security/")
BOT_EMAILS = {"aeonframework@users.noreply.github.com", "aeon@aeonframework.dev"}

def is_bot(n):
    branch_ok = any(n["headRefName"].startswith(p) for p in BRANCH_PREFIXES)
    email = (n.get("commits", {}).get("nodes") or [{}])[0].get("commit", {}).get("author", {}).get("email") or ""
    email_ok = email in BOT_EMAILS
    return branch_ok or email_ok

kept = [n for n in nodes if is_bot(n)]
print(f"Total nodes: {len(nodes)}; bot-filtered: {len(kept)}")

# Fixed "now" for reproducibility — the skill schedule is 10:00 UTC daily
NOW = datetime(2026, 7, 20, 10, 0, 0, tzinfo=timezone.utc)

def parse(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def days_ago(iso):
    return (NOW - parse(iso)).total_seconds() / 86400.0

recent_merges = []
stale_open = []
active_open = []
closed_no_merge = []
fresh_bot = []

for n in kept:
    repo = n["repository"]["nameWithOwner"]
    num = n["number"]
    state = n["state"]
    title = n["title"]
    created = n["createdAt"]
    updated = n["updatedAt"]
    merged = n.get("mergedAt")
    closed = n.get("closedAt")
    age = days_ago(created)
    activity = days_ago(updated)

    entry = {
        "repo": repo, "number": num, "title": title, "state": state,
        "url": n["url"], "createdAt": created, "updatedAt": updated,
        "mergedAt": merged, "closedAt": closed, "headRefName": n["headRefName"],
        "comments": n["comments"]["totalCount"],
        "reviews": n["reviews"]["nodes"],
        "commit_email": (n.get("commits", {}).get("nodes") or [{}])[0].get("commit", {}).get("author", {}).get("email"),
        "age_d": round(age, 2), "activity_d": round(activity, 2),
    }

    if state == "MERGED" and merged and days_ago(merged) <= 7:
        recent_merges.append(entry)
    elif state == "OPEN" and age > 7 and activity > 7:
        stale_open.append(entry)
    elif state == "OPEN":
        active_open.append(entry)
        if age <= 1.0:
            fresh_bot.append(entry)
    elif state == "CLOSED" and closed and days_ago(closed) <= 7:
        closed_no_merge.append(entry)

def key_ts(e):
    return e.get("mergedAt") or e.get("closedAt") or e.get("updatedAt") or e.get("createdAt") or ""

recent_merges.sort(key=key_ts, reverse=True)
stale_open.sort(key=lambda e: e["updatedAt"])
active_open.sort(key=lambda e: e["updatedAt"], reverse=True)
closed_no_merge.sort(key=lambda e: e["closedAt"] or "", reverse=True)

# Canonical hash — sort by (repo, number), tuple (repo, number, state, last-state-ts)
def last_ts(n):
    if n["state"] == "MERGED":
        return n["mergedAt"]
    if n["state"] == "CLOSED":
        return n["closedAt"]
    return n["updatedAt"]

canonical = sorted(
    [(n["repository"]["nameWithOwner"], n["number"], n["state"], last_ts(n)) for n in kept],
    key=lambda t: (t[0], t[1])
)
canon_str = "|".join(f"{r},{n},{s},{t}" for r,n,s,t in canonical)
h = hashlib.sha256(canon_str.encode()).hexdigest()[:16]

result = {
    "now": NOW.isoformat(),
    "total_nodes": len(nodes),
    "kept": len(kept),
    "recent_merges": recent_merges,
    "stale_open": stale_open,
    "active_open": active_open,
    "closed_no_merge": closed_no_merge,
    "fresh_bot": fresh_bot,
    "canonical_str": canon_str,
    "canonical_hash": h,
    "categorization_tuple": (len(recent_merges), len(stale_open), len(closed_no_merge), len(active_open)),
}
pathlib.Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/categorized.json").write_text(json.dumps(result, indent=2))
print(f"\nCategorization: merged(7d)={len(recent_merges)}, stale={len(stale_open)}, closed_no_merge(7d)={len(closed_no_merge)}, active={len(active_open)}, fresh_bot(<24h)={len(fresh_bot)}")
print(f"Canonical hash: {h}")
print(f"Canonical string: {canon_str}")
