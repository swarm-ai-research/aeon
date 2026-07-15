#!/usr/bin/env python3
"""Categorize the PRs fetched into recent-merge / stale-open / active-open / closed-no-merge."""
import json
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime(2026, 7, 15, 10, 22, 0, tzinfo=timezone.utc)
BRANCH_PREFIX = "ai/"
BOT_EMAILS = {"aeonframework@users.noreply.github.com", "aeon@aeonframework.dev"}

data = json.loads(Path(".pending-notify-temp/pr-tracker-raw.json").read_text())
nodes = data["data"]["search"]["nodes"]


def parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else None


def age_days(ts):
    d = parse(ts)
    return (NOW - d).total_seconds() / 86400 if d else None


def matches_bot(pr):
    branch = pr.get("headRefName") or ""
    email = (pr.get("commits", {}).get("nodes", [{}])[0].get("commit", {}).get("author", {}).get("email") or "")
    return branch.startswith(BRANCH_PREFIX) or email in BOT_EMAILS


filtered = [p for p in nodes if matches_bot(p)]
print(f"total_nodes={len(nodes)} matched={len(filtered)}")

buckets = {"recent_merged": [], "stale_open": [], "active_open": [], "closed_no_merge": []}

for pr in filtered:
    repo = pr["repository"]["nameWithOwner"]
    n = pr["number"]
    state = pr["state"]
    created_age = age_days(pr["createdAt"])
    updated_age = age_days(pr["updatedAt"])
    merged_age = age_days(pr["mergedAt"]) if pr.get("mergedAt") else None
    closed_age = age_days(pr["closedAt"]) if pr.get("closedAt") else None
    entry = {
        "repo": repo, "number": n, "title": pr["title"], "state": state,
        "url": pr["url"], "headRefName": pr["headRefName"],
        "createdAt": pr["createdAt"], "updatedAt": pr["updatedAt"],
        "mergedAt": pr.get("mergedAt"), "closedAt": pr.get("closedAt"),
        "created_age_d": round(created_age, 2),
        "updated_age_d": round(updated_age, 2),
        "merged_age_d": round(merged_age, 2) if merged_age is not None else None,
        "closed_age_d": round(closed_age, 2) if closed_age is not None else None,
        "commit_email": pr["commits"]["nodes"][0]["commit"]["author"]["email"] if pr["commits"]["nodes"] else "",
    }
    if state == "MERGED" and merged_age is not None and merged_age <= 7:
        buckets["recent_merged"].append(entry)
    elif state == "OPEN":
        if created_age > 7 and updated_age > 7:
            buckets["stale_open"].append(entry)
        else:
            buckets["active_open"].append(entry)
    elif state == "CLOSED" and closed_age is not None and closed_age <= 7:
        buckets["closed_no_merge"].append(entry)


summary = {
    "now_utc": NOW.isoformat().replace("+00:00", "Z"),
    "counts": {k: len(v) for k, v in buckets.items()},
    "buckets": buckets,
    "trigger_hash_input": [
        (p["repository"]["nameWithOwner"], p["number"], p["state"],
         p.get("mergedAt") or p.get("closedAt") or p.get("updatedAt"))
        for p in filtered
    ],
}
Path(".pending-notify-temp/pr-tracker-classified.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary["counts"]))
print(json.dumps(summary["trigger_hash_input"]))
