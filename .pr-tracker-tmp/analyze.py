#!/usr/bin/env python3
"""pr-tracker analyze: filter, categorize, hash, decide-notify."""
import json, hashlib, pathlib
from datetime import datetime, timezone

TODAY = "2026-07-25"
NOW = datetime(2026, 7, 25, 10, 0, 0, tzinfo=timezone.utc)  # ~10:00Z run

BRANCH_PREFIXES = ("ai/", "security/", "fix/security/", "aeon/")
BOT_EMAILS = {
    "aeonframework@users.noreply.github.com",
    "aeon@aeonframework.dev",
    "aeonframework@proton.me",
    "security@aeonframework.dev",
}

raw = json.loads(pathlib.Path(".pr-tracker-tmp/raw.json").read_text())
nodes = raw["data"]["search"]["nodes"]

def bot_email(n):
    cs = n.get("commits", {}).get("nodes", [])
    if not cs: return ""
    return (cs[0].get("commit", {}).get("author", {}) or {}).get("email", "") or ""

def parse(ts):
    if not ts: return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def days_between(later, earlier):
    return (later - earlier).total_seconds() / 86400.0

kept = []
dropped = []
for n in nodes:
    if not n: continue
    head = n.get("headRefName", "") or ""
    email = bot_email(n)
    branch_ok = any(head.startswith(p) for p in BRANCH_PREFIXES)
    email_ok = email in BOT_EMAILS
    if branch_ok or email_ok:
        kept.append(n)
    else:
        dropped.append({"repo": n["repository"]["nameWithOwner"], "num": n["number"], "head": head, "email": email})

# Categorize
recent_merges, stale_open, active_open, closed_nomerge, still_open, closed_beyond = [], [], [], [], [], []
for n in kept:
    state = n["state"]
    repo = n["repository"]["nameWithOwner"]
    num = n["number"]
    created = parse(n["createdAt"])
    updated = parse(n["updatedAt"])
    merged = parse(n.get("mergedAt"))
    closed = parse(n.get("closedAt"))
    last_review = n.get("reviews", {}).get("nodes", [])
    last_review_at = parse(last_review[0].get("submittedAt")) if last_review else None
    last_activity = updated
    if last_review_at and last_review_at > last_activity:
        last_activity = last_review_at
    age_d = days_between(NOW, created)
    activity_age_d = days_between(NOW, last_activity)
    row = {
        "repo": repo, "num": num, "title": n["title"], "state": state,
        "head": n["headRefName"], "url": n["url"], "email": bot_email(n),
        "createdAt": n["createdAt"], "updatedAt": n["updatedAt"],
        "mergedAt": n.get("mergedAt"), "closedAt": n.get("closedAt"),
        "age_d": round(age_d, 2), "activity_age_d": round(activity_age_d, 2),
        "comments": n.get("comments", {}).get("totalCount", 0),
        "last_review_state": (last_review[0].get("state") if last_review else None),
        "last_review_at": (last_review[0].get("submittedAt") if last_review else None),
    }
    if state == "MERGED":
        merged_age = days_between(NOW, merged)
        row["merged_age_d"] = round(merged_age, 2)
        if merged_age <= 7: recent_merges.append(row)
        else: closed_beyond.append(row)  # still retained in table for 30d
    elif state == "OPEN":
        still_open.append(row)
        if age_d > 7 and activity_age_d > 7:
            stale_open.append(row)
        else:
            active_open.append(row)
    elif state == "CLOSED":
        closed_age = days_between(NOW, closed)
        row["closed_age_d"] = round(closed_age, 2)
        if closed_age <= 7: closed_nomerge.append(row)
        else: closed_beyond.append(row)

def sort_key(r):
    return (-days_between(NOW, parse(r["createdAt"])), r["repo"], r["num"])

# Hash: sha256[:16] over sorted repo#num:state:updatedAt tuples
all_rows = recent_merges + stale_open + active_open + closed_nomerge + closed_beyond
tuples = sorted(f"{r['repo']}#{r['num']}:{r['state']}:{r['updatedAt']}" for r in all_rows)
digest = hashlib.sha256("|".join(tuples).encode()).hexdigest()[:16]

# Fresh bot PRs (<24h since createdAt)
fresh = [r for r in all_rows if days_between(NOW, parse(r["createdAt"])) < 1.0]

out = {
    "today": TODAY,
    "now_iso": NOW.isoformat().replace("+00:00", "Z"),
    "author": "aeonframework",
    "branch_prefixes": list(BRANCH_PREFIXES),
    "bot_emails": sorted(BOT_EMAILS),
    "node_count": len(nodes),
    "kept_count": len(kept),
    "dropped_count": len(dropped),
    "dropped_examples": dropped[:5],
    "recent_merges": recent_merges,
    "stale_open": stale_open,
    "active_open": sorted(active_open, key=lambda r: r["createdAt"]),
    "closed_nomerge": closed_nomerge,
    "all_open": sorted(still_open, key=lambda r: r["createdAt"]),
    "retained_beyond_window": closed_beyond,
    "tuple": (len(recent_merges), len(stale_open), len(closed_nomerge), len(active_open)),
    "hash": digest,
    "fresh_bot_prs_lt24h": fresh,
    "fresh_bot_prs_count": len(fresh),
}

pathlib.Path(".pr-tracker-tmp/result.json").write_text(json.dumps(out, indent=2, default=str))
print(json.dumps({
    "nodes": len(nodes), "kept": len(kept), "dropped": len(dropped),
    "tuple": out["tuple"], "hash": digest, "fresh_lt24h": len(fresh),
    "open": len(still_open), "merges_7d": len(recent_merges),
    "stale": len(stale_open), "closed_nomerge_7d": len(closed_nomerge),
}, indent=2))
