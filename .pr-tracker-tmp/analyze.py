#!/usr/bin/env python3
"""Categorize PRs, compute tuple hash, decide notify."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

TODAY = "2026-07-22"
NOW = datetime.fromisoformat(f"{TODAY}T09:20:00+00:00")

# Bot identity heuristic (memory-widened, matches actual live queue)
BOT_EMAILS = {
    "aeonframework@users.noreply.github.com",
    "aeon@aeonframework.dev",
}
BOT_PREFIXES = ("ai/", "security/")

raw = json.loads(Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/raw.json").read_text())
nodes = raw["data"]["search"]["nodes"]

# Filter to bot-authored via OR-widened rule
def is_bot(n):
    branch = n.get("headRefName") or ""
    commits = n.get("commits", {}).get("nodes") or []
    email = ""
    if commits:
        email = ((commits[0].get("commit") or {}).get("author") or {}).get("email") or ""
    return branch.startswith(BOT_PREFIXES) or email in BOT_EMAILS

bot_prs = [n for n in nodes if is_bot(n)]

def parse(ts):
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def days_since(ts):
    dt = parse(ts)
    if dt is None:
        return None
    return (NOW - dt).total_seconds() / 86400

# Categorize
recent_merges = []   # MERGED, mergedAt within 7d
stale_open = []      # OPEN, createdAt > 7d ago, no activity in last 7d
active_open = []     # OPEN, createdAt < 7d ago OR recent activity
closed_no_merge = [] # CLOSED (not merged), closedAt within 7d

for pr in bot_prs:
    state = pr["state"]
    repo = pr["repository"]["nameWithOwner"]
    num = pr["number"]
    if state == "MERGED":
        age = days_since(pr.get("mergedAt"))
        if age is not None and age <= 30:
            recent_merges.append(pr)  # keep merged in 30d table; 7d subset used for notify
    elif state == "OPEN":
        created_age = days_since(pr["createdAt"])
        updated_age = days_since(pr.get("updatedAt"))
        # activity signal: comments / reviews on last 7d
        review_nodes = (pr.get("reviews") or {}).get("nodes") or []
        last_review_age = None
        if review_nodes:
            last_review_age = days_since(review_nodes[0].get("submittedAt"))
        recent_activity = (updated_age is not None and updated_age <= 7) or \
                          (last_review_age is not None and last_review_age <= 7)
        if created_age is not None and created_age > 7 and not recent_activity:
            stale_open.append(pr)
        else:
            active_open.append(pr)
    elif state == "CLOSED":
        # closed w/o merge
        age = days_since(pr.get("closedAt"))
        if age is not None and age <= 30:
            closed_no_merge.append(pr)

# Sort each list
recent_merges.sort(key=lambda p: p.get("mergedAt") or "", reverse=True)
stale_open.sort(key=lambda p: p.get("updatedAt") or "", reverse=True)
active_open.sort(key=lambda p: p.get("createdAt") or "", reverse=True)
closed_no_merge.sort(key=lambda p: p.get("closedAt") or "", reverse=True)

# Tuple hash for step-5 dedup
tuples = []
for pr in sorted(bot_prs, key=lambda p: (p["repository"]["nameWithOwner"], p["number"])):
    state = pr["state"]
    if state == "MERGED":
        ts = pr.get("mergedAt") or ""
    elif state == "CLOSED":
        ts = pr.get("closedAt") or ""
    else:
        ts = pr.get("updatedAt") or ""
    tuples.append(f"{pr['repository']['nameWithOwner']}#{pr['number']}:{state}:{ts}")
canonical = "|".join(tuples)
tuple_hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]

# Fresh-bot-PR trigger: any bot PR filed in last 24h
fresh_bot_prs = [p for p in bot_prs
                 if (days_since(p["createdAt"]) or 999) <= 1.0]

# 7d-scoped counts for notify
merges_7d = [p for p in recent_merges if (days_since(p.get("mergedAt")) or 999) <= 7]
closed_7d = [p for p in closed_no_merge if (days_since(p.get("closedAt")) or 999) <= 7]

result = {
    "today": TODAY,
    "now_iso": NOW.isoformat(),
    "n_nodes": len(nodes),
    "n_bot": len(bot_prs),
    "tuple_hash": tuple_hash,
    "canonical": canonical,
    "categorization": {
        "recent_merges_7d": [
            {"repo": p["repository"]["nameWithOwner"], "num": p["number"],
             "title": p["title"], "url": p["url"],
             "opened": p["createdAt"][:10], "merged": (p.get("mergedAt") or "")[:10]}
            for p in merges_7d
        ],
        "recent_merges_30d": [
            {"repo": p["repository"]["nameWithOwner"], "num": p["number"],
             "title": p["title"], "url": p["url"],
             "opened": p["createdAt"][:10], "merged": (p.get("mergedAt") or "")[:10]}
            for p in recent_merges
        ],
        "stale_open": [
            {"repo": p["repository"]["nameWithOwner"], "num": p["number"],
             "title": p["title"], "url": p["url"],
             "opened": p["createdAt"][:10],
             "age_days": round(days_since(p["createdAt"]) or 0, 2),
             "last_activity_days": round(days_since(p.get("updatedAt")) or 0, 2)}
            for p in stale_open
        ],
        "active_open": [
            {"repo": p["repository"]["nameWithOwner"], "num": p["number"],
             "title": p["title"], "url": p["url"],
             "opened": p["createdAt"][:10],
             "age_days": round(days_since(p["createdAt"]) or 0, 2),
             "last_activity_days": round(days_since(p.get("updatedAt")) or 0, 2),
             "comments": (p.get("comments") or {}).get("totalCount", 0),
             "last_review": ((p.get("reviews") or {}).get("nodes") or [{}])[0].get("state") if (p.get("reviews") or {}).get("nodes") else None,
             "head_branch": p.get("headRefName")}
            for p in active_open
        ],
        "closed_no_merge_7d": [
            {"repo": p["repository"]["nameWithOwner"], "num": p["number"],
             "title": p["title"], "url": p["url"],
             "closed": (p.get("closedAt") or "")[:10]}
            for p in closed_7d
        ],
        "closed_no_merge_30d": [
            {"repo": p["repository"]["nameWithOwner"], "num": p["number"],
             "title": p["title"], "url": p["url"],
             "closed": (p.get("closedAt") or "")[:10]}
            for p in closed_no_merge
        ],
    },
    "fresh_bot_prs": [
        {"repo": p["repository"]["nameWithOwner"], "num": p["number"],
         "title": p["title"], "age_days": round(days_since(p["createdAt"]) or 0, 2)}
        for p in fresh_bot_prs
    ],
}

# Yesterday's hash for comparison
result["prior_hash"] = "a55567402362e9bc"  # from 2026-07-21 pr-status.md line 50
result["hash_matches_prior"] = (tuple_hash == result["prior_hash"])

# Notify decision
n_merges_7d = len(merges_7d)
n_stale = len(stale_open)
n_closed_7d = len(closed_7d)
n_active = len(active_open)
result["counts"] = {
    "merges_7d": n_merges_7d,
    "stale_open": n_stale,
    "closed_no_merge_7d": n_closed_7d,
    "active_open": n_active,
}

# SKILL.md step-5: Skip if 0 merges AND 0 stale AND 0 closed-no-merge.
step5_content_send = not (n_merges_7d == 0 and n_stale == 0 and n_closed_7d == 0)
# Memory-doc'd hash-based dedup guard: SKIP even if content warrants, when hash matches prior day.
hash_skip = result["hash_matches_prior"]
# Memory-doc'd fresh-bot-PR trigger override: SEND if a bot PR was filed in last 24h even if hash matches
fresh_override = len(fresh_bot_prs) > 0

if step5_content_send and not hash_skip:
    decision = "SEND"
    reason = "step-5 content trigger fires, hash differs from prior"
elif step5_content_send and hash_skip and fresh_override:
    decision = "SEND"
    reason = "hash matches prior but fresh-bot-PR trigger fires"
elif step5_content_send and hash_skip:
    decision = "SKIP"
    reason = "step-5 would send but tuple-identity hash matches prior day — dedup guard"
elif not step5_content_send and fresh_override:
    decision = "SEND"
    reason = "no step-5 content, but fresh-bot-PR trigger fires"
else:
    decision = "SKIP"
    reason = "no step-5 content and no fresh-bot-PR"

result["notify"] = {"decision": decision, "reason": reason,
                    "step5_content_send": step5_content_send,
                    "hash_matches_prior": hash_skip,
                    "fresh_override": fresh_override}

out = Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/analysis.json")
out.write_text(json.dumps(result, indent=2))

# Print human summary
print(f"TODAY={TODAY}")
print(f"n_nodes={len(nodes)}  n_bot={len(bot_prs)}")
print(f"tuple_hash={tuple_hash}  prior_hash={result['prior_hash']}  match={result['hash_matches_prior']}")
print(f"counts: merges_7d={n_merges_7d} stale={n_stale} closed_no_merge_7d={n_closed_7d} active={n_active}")
print(f"fresh_bot_prs={len(fresh_bot_prs)}")
print(f"NOTIFY: {decision} — {reason}")
print()
print("=== Bot PRs ===")
for pr in sorted(bot_prs, key=lambda p: (p["repository"]["nameWithOwner"], p["number"])):
    email = ""
    commits = pr.get("commits", {}).get("nodes") or []
    if commits:
        email = ((commits[0].get("commit") or {}).get("author") or {}).get("email") or ""
    print(f"  {pr['repository']['nameWithOwner']}#{pr['number']} {pr['state']:8s} branch={pr['headRefName']} email={email}")
    print(f"    title={pr['title']}")
    print(f"    createdAt={pr['createdAt']} updatedAt={pr.get('updatedAt')} mergedAt={pr.get('mergedAt')} closedAt={pr.get('closedAt')}")
