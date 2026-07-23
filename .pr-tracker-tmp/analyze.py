#!/usr/bin/env python3
"""Analyze PR fetch results and produce categorization + notification content."""
import json
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

TODAY = "2026-07-23"
NOW = datetime(2026, 7, 23, 12, 0, tzinfo=timezone.utc)  # approximate; refined below
SEVEN_DAYS = timedelta(days=7)
THIRTY_DAYS = timedelta(days=30)

# Bot identity list per [[aeon-bot-uses-multiple-signing-identities]]
# NEW 2026-07-23: aeonframework@proton.me added — third signing identity discovered
# via koala73/worldmonitor#5477 (branch fix/security/sharp-cve-blog-site).
KNOWN_BOT_EMAILS = {
    "aeonframework@users.noreply.github.com",
    "aeon@aeonframework.dev",
    "aeonframework@proton.me",
}
BRANCH_PREFIXES = ("ai/", "security/", "fix/security/")

raw = json.loads(Path(".pr-tracker-tmp/raw.json").read_text())
nodes = raw.get("data", {}).get("search", {}).get("nodes", [])

# OR-filter: branch prefix OR bot email
def is_bot_pr(n):
    branch = n.get("headRefName", "") or ""
    if any(branch.startswith(p) for p in BRANCH_PREFIXES):
        return True
    commits = n.get("commits", {}).get("nodes", [])
    if commits:
        email = commits[0].get("commit", {}).get("author", {}).get("email", "") or ""
        if email in KNOWN_BOT_EMAILS:
            return True
    return False

bot_prs = [n for n in nodes if is_bot_pr(n)]

def parse_dt(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def days_since(dt):
    if dt is None:
        return None
    return (NOW - dt).total_seconds() / 86400

# Categorize
recent_merges = []  # merged in last 7d
stale_open = []     # open >7d with no activity in 7d
active_open = []    # open <7d or recent activity
closed_no_merge_7d = []  # closed unmerged in last 7d
merged_30d = []
closed_30d = []

for pr in bot_prs:
    state = pr["state"]
    created = parse_dt(pr["createdAt"])
    updated = parse_dt(pr["updatedAt"])
    merged = parse_dt(pr.get("mergedAt"))
    closed = parse_dt(pr.get("closedAt"))
    reviews = pr.get("reviews", {}).get("nodes", [])
    last_review = parse_dt(reviews[0]["submittedAt"]) if reviews else None
    last_activity = max(x for x in [updated, last_review] if x is not None)

    entry = {
        "repo": pr["repository"]["nameWithOwner"],
        "number": pr["number"],
        "title": pr["title"],
        "url": pr["url"],
        "state": state,
        "headRefName": pr.get("headRefName", ""),
        "createdAt": created,
        "updatedAt": updated,
        "mergedAt": merged,
        "closedAt": closed,
        "last_activity": last_activity,
        "comments": pr.get("comments", {}).get("totalCount", 0),
        "last_review_state": reviews[0]["state"] if reviews else None,
        "commit_email": (pr.get("commits", {}).get("nodes", [{}])[0].get("commit", {}).get("author", {}).get("email", "") if pr.get("commits", {}).get("nodes") else ""),
    }

    if state == "MERGED":
        if NOW - merged <= SEVEN_DAYS:
            recent_merges.append(entry)
        if NOW - merged <= THIRTY_DAYS:
            merged_30d.append(entry)
    elif state == "OPEN":
        age = NOW - created
        activity_age = NOW - last_activity
        if age > SEVEN_DAYS and activity_age > SEVEN_DAYS:
            stale_open.append(entry)
        else:
            active_open.append(entry)
    elif state == "CLOSED":
        if closed and NOW - closed <= SEVEN_DAYS:
            closed_no_merge_7d.append(entry)
        if closed and NOW - closed <= THIRTY_DAYS:
            closed_30d.append(entry)

# All open (for table)
open_all = stale_open + active_open

# Canonical hash for step-5 dedup guard
tuples = sorted(
    (e["repo"], e["number"], e["state"], (e["updatedAt"] or e["createdAt"]).isoformat())
    for e in [*open_all, *merged_30d, *closed_30d]
)
canon = "|".join(f"{r}#{n}:{s}:{t}" for r, n, s, t in tuples)
canon_hash = hashlib.sha256(canon.encode()).hexdigest()[:16]

def fmt(dt, days_only=False):
    if dt is None:
        return "-"
    if days_only:
        return dt.date().isoformat()
    return dt.isoformat()

def age_days(dt):
    return (NOW - dt).total_seconds() / 86400

# Fresh-bot-PR trigger: any PR filed <24h ago
fresh_bot_pr = any(
    (NOW - e["createdAt"]) < timedelta(days=1) for e in open_all
)

# Save results
out = {
    "today": TODAY,
    "counts": {
        "open": len(open_all),
        "recent_merges_7d": len(recent_merges),
        "stale_open": len(stale_open),
        "active_open": len(active_open),
        "closed_no_merge_7d": len(closed_no_merge_7d),
        "merged_30d": len(merged_30d),
        "closed_30d": len(closed_30d),
    },
    "canon_hash": canon_hash,
    "fresh_bot_pr": fresh_bot_pr,
    "open": [
        {
            "repo": e["repo"],
            "number": e["number"],
            "title": e["title"],
            "url": e["url"],
            "opened": fmt(e["createdAt"], True),
            "age_days": round(age_days(e["createdAt"]), 2),
            "activity_days_ago": round(age_days(e["last_activity"]), 2),
            "activity_summary": f"{e['comments']} comments; last touch {age_days(e['last_activity']):.2f}d ago" + (f" ({e['last_review_state']})" if e["last_review_state"] else ""),
            "bucket": "stale" if (NOW - e["createdAt"] > SEVEN_DAYS and NOW - e["last_activity"] > SEVEN_DAYS) else "active",
        }
        for e in sorted(open_all, key=lambda x: x["createdAt"])
    ],
    "recent_merges_7d": [
        {"repo": e["repo"], "number": e["number"], "title": e["title"], "url": e["url"], "opened": fmt(e["createdAt"], True), "merged": fmt(e["mergedAt"], True)}
        for e in recent_merges
    ],
    "merged_30d": [
        {"repo": e["repo"], "number": e["number"], "title": e["title"], "url": e["url"], "opened": fmt(e["createdAt"], True), "merged": fmt(e["mergedAt"], True)}
        for e in merged_30d
    ],
    "closed_no_merge_7d": [
        {"repo": e["repo"], "number": e["number"], "title": e["title"], "url": e["url"], "closed": fmt(e["closedAt"], True)}
        for e in closed_no_merge_7d
    ],
    "closed_30d": [
        {"repo": e["repo"], "number": e["number"], "title": e["title"], "url": e["url"], "closed": fmt(e["closedAt"], True)}
        for e in closed_30d
    ],
}

Path(".pr-tracker-tmp/analysis.json").write_text(json.dumps(out, indent=2, default=str))
print(f"nodes_returned={len(nodes)}")
print(f"bot_prs_kept={len(bot_prs)}")
print(f"canon_hash={canon_hash}")
print(f"open={len(open_all)} (stale={len(stale_open)}, active={len(active_open)})")
print(f"recent_merges_7d={len(recent_merges)}")
print(f"closed_no_merge_7d={len(closed_no_merge_7d)}")
print(f"fresh_bot_pr={fresh_bot_pr}")
