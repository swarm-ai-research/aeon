#!/usr/bin/env python3
"""Categorize bot PRs into buckets and print a snapshot."""
import json
from datetime import datetime, timezone
from pathlib import Path

TODAY = "2026-08-13"
NOW = datetime(2026, 8, 13, 11, 0, 0, tzinfo=timezone.utc)  # nominal scan time
PREFIXES = ("ai/", "security/", "fix/security/", "aeon/")
STALE_BOT_LOGINS = {"github-actions", "dependabot", "stale-bot"}
STALE_NOTICE_FRAGMENTS = [
    "This PR is stale because it has been open",
    "This issue has been automatically marked as stale",
    "marked as stale because it has not had",
]

def parse(dt):
    if not dt:
        return None
    return datetime.fromisoformat(dt.replace("Z", "+00:00"))

def days_since(dt):
    if not dt:
        return None
    return (NOW - parse(dt)).total_seconds() / 86400

def is_stale_bot_comment(c):
    login = ((c.get("author") or {}).get("login") or "").replace("[bot]", "")
    if login not in STALE_BOT_LOGINS:
        return False
    body = c.get("bodyText") or ""
    return any(f in body for f in STALE_NOTICE_FRAGMENTS)

def substantive_last_activity(pr):
    """Return the latest updatedAt-like timestamp EXCLUDING stale-bot comments."""
    ts = parse(pr["createdAt"])
    # Consider reviews
    for r in (pr.get("reviews") or {}).get("nodes") or []:
        rt = parse(r.get("submittedAt"))
        if rt and rt > ts:
            ts = rt
    # Consider non-stale-bot comments
    for c in (pr.get("comments") or {}).get("nodes") or []:
        if is_stale_bot_comment(c):
            continue
        ct = parse(c.get("createdAt"))
        if ct and ct > ts:
            ts = ct
    return ts

def bucket(pr):
    state = pr["state"]
    created = parse(pr["createdAt"])
    age = (NOW - created).total_seconds() / 86400
    if state == "MERGED":
        m = days_since(pr["mergedAt"])
        return ("recent_merges" if m <= 7 else "old_merges"), age
    if state == "CLOSED":
        c = days_since(pr["closedAt"])
        return ("closed_no_merge" if c <= 30 else "old_closed"), age
    # OPEN
    sub = substantive_last_activity(pr)
    inactivity = (NOW - sub).total_seconds() / 86400
    if age > 7 and inactivity > 7:
        return "stale_open", age
    return "active_open", age

def main():
    data = json.loads((Path(__file__).parent / "graphql.json").read_text())
    nodes = data["data"]["search"]["nodes"]
    bot_prs = [n for n in nodes if (n.get("headRefName") or "").startswith(PREFIXES)]
    buckets = {"recent_merges": [], "old_merges": [], "closed_no_merge": [],
               "old_closed": [], "active_open": [], "stale_open": []}
    for pr in bot_prs:
        b, age = bucket(pr)
        pr["_bucket"] = b
        pr["_age"] = age
        buckets[b].append(pr)
    for name, prs in buckets.items():
        prs.sort(key=lambda p: p["updatedAt"], reverse=True)
        print(f"== {name} ({len(prs)}) ==")
        for pr in prs:
            repo = pr["repository"]["nameWithOwner"]
            arch = " [ARCHIVED]" if pr["repository"].get("isArchived") else ""
            merged = pr.get("mergedAt") or ""
            closed = pr.get("closedAt") or ""
            head = pr["headRefName"]
            title = pr["title"][:80]
            print(f"  {repo}#{pr['number']} state={pr['state']} age={pr['_age']:.1f}d "
                  f"created={pr['createdAt'][:10]} merged={merged[:10]} closed={closed[:10]} "
                  f"head={head}{arch}")
            print(f"    -> {title}")
    # Write bucket file
    out = {k: [{"repo": p["repository"]["nameWithOwner"],
                "number": p["number"],
                "title": p["title"],
                "url": p["url"],
                "createdAt": p["createdAt"],
                "mergedAt": p.get("mergedAt"),
                "closedAt": p.get("closedAt"),
                "updatedAt": p.get("updatedAt"),
                "headRefName": p["headRefName"],
                "age_days": p["_age"],
                "state": p["state"],
                "commentsTotal": (p.get("comments") or {}).get("totalCount", 0),
                "lastReviewState": ((p.get("reviews") or {}).get("nodes") or [{}])[0].get("state"),
                "isArchived": p["repository"].get("isArchived", False),
                }
               for p in v]
           for k, v in buckets.items()}
    (Path(__file__).parent / "buckets.json").write_text(json.dumps(out, indent=2))
    print("wrote buckets.json")

if __name__ == "__main__":
    main()
