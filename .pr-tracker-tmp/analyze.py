#!/usr/bin/env python3
"""Categorize PRs and compute the dedup hash for notify decision."""
import json
import hashlib
import pathlib
from datetime import datetime, timezone, timedelta

TODAY = datetime(2026, 7, 21, 10, 0, 0, tzinfo=timezone.utc)
data = json.loads(pathlib.Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/raw.json").read_text())
nodes = data["data"]["search"]["nodes"]

# Sort by (repo, number) for deterministic hash
nodes_sorted = sorted(nodes, key=lambda n: (n["repository"]["nameWithOwner"], n["number"]))

# Build canonical tuple list (repo, number, state, most-recent-timestamp)
def key_ts(n):
    # Use mergedAt/closedAt if terminal, else updatedAt
    if n["state"] == "MERGED":
        return n.get("mergedAt") or n["updatedAt"]
    if n["state"] == "CLOSED":
        return n.get("closedAt") or n["updatedAt"]
    return n["updatedAt"]

tuples = []
for n in nodes_sorted:
    ts = key_ts(n)
    tuples.append((n["repository"]["nameWithOwner"], n["number"], n["state"], ts))

canonical = "|".join(f"{r}#{num}:{st}:{ts}" for (r, num, st, ts) in tuples)
h = hashlib.sha256(canonical.encode()).hexdigest()[:16]

print("=== Canonical tuples ===")
for t in tuples:
    print(f"  {t}")
print(f"\ncanonical_hash = {h}")
print(f"yesterday_hash = c267efaeed220887 (per memory/topics/pr-status.md)")
print(f"hash_changed   = {h != 'c267efaeed220887'}")

# Categorize
def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

merged_7d = []
stale_open = []
active_open = []
closed_no_merge_7d = []

for n in nodes:
    repo = n["repository"]["nameWithOwner"]
    num = n["number"]
    created = parse_ts(n["createdAt"])
    updated = parse_ts(n["updatedAt"])
    days_since_updated = (TODAY - updated).total_seconds() / 86400
    days_since_created = (TODAY - created).total_seconds() / 86400

    if n["state"] == "MERGED":
        merged = parse_ts(n["mergedAt"])
        days_since_merged = (TODAY - merged).total_seconds() / 86400
        if days_since_merged <= 7:
            merged_7d.append((repo, num, n["title"], n["createdAt"][:10], n["mergedAt"][:10]))
    elif n["state"] == "CLOSED":
        closed = parse_ts(n["closedAt"])
        days_since_closed = (TODAY - closed).total_seconds() / 86400
        if days_since_closed <= 7:
            closed_no_merge_7d.append((repo, num, n["title"], n["closedAt"][:10]))
    elif n["state"] == "OPEN":
        if days_since_created > 7 and days_since_updated > 7:
            stale_open.append((repo, num, n["title"], n["createdAt"][:10], round(days_since_created, 2), round(days_since_updated, 2)))
        else:
            active_open.append((repo, num, n["title"], n["createdAt"][:10], round(days_since_created, 2), round(days_since_updated, 2)))

print("\n=== Categories ===")
print(f"Recent merges (7d): {len(merged_7d)}")
for x in merged_7d: print(f"  {x}")
print(f"Stale open (>7d): {len(stale_open)}")
for x in stale_open: print(f"  {x}")
print(f"Active open: {len(active_open)}")
for x in active_open: print(f"  {x}")
print(f"Closed no-merge (7d): {len(closed_no_merge_7d)}")
for x in closed_no_merge_7d: print(f"  {x}")

# Decision
print("\n=== Notify decision ===")
step5_would_send = not (len(merged_7d) == 0 and len(stale_open) == 0 and len(closed_no_merge_7d) == 0)
hash_changed = h != "c267efaeed220887"
fresh_bot_pr = any((TODAY - parse_ts(n["createdAt"])).total_seconds() / 86400 < 1 for n in nodes)
print(f"step5_would_send (any of merged/stale/closed non-zero) = {step5_would_send}")
print(f"hash_changed (per pr-tracker-notify-repeats dedup)      = {hash_changed}")
print(f"fresh_bot_pr (<24h old)                                 = {fresh_bot_pr}")

# Per memory's dedup guard: send only if hash changed OR fresh bot PR trigger
send = hash_changed or fresh_bot_pr
print(f"\nFINAL: {'SEND' if send else 'SKIP'} — {'hash unchanged and no fresh PR' if not send else ('hash changed' if hash_changed else 'fresh bot PR')}")

# Persist categorization JSON for downstream steps
out = {
    "today": "2026-07-21",
    "hash": h,
    "yesterday_hash": "c267efaeed220887",
    "hash_changed": hash_changed,
    "fresh_bot_pr": fresh_bot_pr,
    "send": send,
    "merged_7d": [{"repo": r, "number": n, "title": t, "created": c, "merged": m} for (r, n, t, c, m) in merged_7d],
    "stale_open": [{"repo": r, "number": n, "title": t, "created": c, "age_d": ac, "quiet_d": au} for (r, n, t, c, ac, au) in stale_open],
    "active_open": [{"repo": r, "number": n, "title": t, "created": c, "age_d": ac, "quiet_d": au} for (r, n, t, c, ac, au) in active_open],
    "closed_no_merge_7d": [{"repo": r, "number": n, "title": t, "closed": cl} for (r, n, t, cl) in closed_no_merge_7d],
    "all_prs": [
        {"repo": n["repository"]["nameWithOwner"], "number": n["number"], "title": n["title"], "state": n["state"], "head": n["headRefName"], "url": n["url"], "created": n["createdAt"], "updated": n["updatedAt"], "merged": n.get("mergedAt"), "closed": n.get("closedAt"), "comments": n["comments"]["totalCount"], "last_review": (n["reviews"]["nodes"][0]["state"] if n["reviews"]["nodes"] else None), "commit_email": (n["commits"]["nodes"][0]["commit"]["author"]["email"] if n["commits"]["nodes"] else None)}
        for n in nodes_sorted
    ],
}
pathlib.Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/categorized.json").write_text(json.dumps(out, indent=2))
print(f"\nWrote categorized.json")
