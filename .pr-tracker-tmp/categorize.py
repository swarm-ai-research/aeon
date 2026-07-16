import json, datetime as dt, hashlib
data = json.load(open("/home/runner/work/aeon/aeon/.pr-tracker-tmp/raw.json"))
nodes = data["data"]["search"]["nodes"]

BOT_EMAILS = {"aeonframework@users.noreply.github.com","aeon@aeonframework.dev"}
BRANCH_PREFIX = "ai/"

def is_bot_pr(n):
    branch = (n.get("headRefName") or "")
    commits = n.get("commits",{}).get("nodes",[])
    email = commits[0]["commit"]["author"]["email"] if commits else ""
    return branch.startswith(BRANCH_PREFIX) or (email in BOT_EMAILS)

bot_prs = [n for n in nodes if is_bot_pr(n)]
print("Bot PRs (after OR-filter):", len(bot_prs))

NOW = dt.datetime(2026,7,16,10,0,0, tzinfo=dt.timezone.utc)
def parse(x):
    return dt.datetime.fromisoformat(x.replace("Z","+00:00")) if x else None
def days_ago(x):
    d = parse(x)
    return None if d is None else (NOW - d).total_seconds()/86400

recent_merges, stale_open, active_open, closed_no_merge = [], [], [], []

for n in bot_prs:
    state = n["state"]
    entry = {
        "repo": n["repository"]["nameWithOwner"],
        "number": n["number"],
        "title": n["title"],
        "state": state,
        "created": n["createdAt"],
        "merged": n.get("mergedAt"),
        "closed": n.get("closedAt"),
        "updated": n.get("updatedAt"),
        "url": n["url"],
        "created_days": days_ago(n["createdAt"]),
        "merged_days": days_ago(n.get("mergedAt")) if n.get("mergedAt") else None,
        "closed_days": days_ago(n.get("closedAt")) if n.get("closedAt") else None,
        "updated_days": days_ago(n.get("updatedAt")) if n.get("updatedAt") else None,
        "comments": n.get("comments",{}).get("totalCount",0),
    }
    if state == "MERGED":
        if entry["merged_days"] is not None and entry["merged_days"] <= 7:
            recent_merges.append(entry)
    elif state == "CLOSED":
        if entry["closed_days"] is not None and entry["closed_days"] <= 7:
            closed_no_merge.append(entry)
    elif state == "OPEN":
        stale = (entry["created_days"] or 0) > 7 and (entry["updated_days"] or 0) > 7
        if stale:
            stale_open.append(entry)
        else:
            active_open.append(entry)

print("Recent merges (7d):", len(recent_merges))
print("Stale open (>7d):", len(stale_open))
print("Active open:", len(active_open))
print("Closed no-merge (7d):", len(closed_no_merge))
print()
for label, arr in [("MERGED-recent",recent_merges),("STALE-OPEN",stale_open),("ACTIVE-OPEN",active_open),("CLOSED-NOMERGE",closed_no_merge)]:
    for e in arr:
        cd = e["created_days"] if e["created_days"] is not None else -1
        ud = e["updated_days"] if e["updated_days"] is not None else -1
        print(f"  [{label}] {e['repo']}#{e['number']} — {e['title']} (created_days={cd:.2f}, updated_days={ud:.2f})")

print()
print("--- All bot PRs (for 30d tables) ---")
for n in bot_prs:
    ud = days_ago(n.get("updatedAt"))
    cd = days_ago(n.get("createdAt"))
    md = days_ago(n.get("mergedAt")) if n.get("mergedAt") else None
    cld = days_ago(n.get("closedAt")) if n.get("closedAt") else None
    print(f"  {n['repository']['nameWithOwner']}#{n['number']} state={n['state']} created={n['createdAt']} merged={n.get('mergedAt')} closed={n.get('closedAt')} updated_days={ud:.2f} created_days={cd:.2f} merged_days={md} closed_days={cld}")

key_tuples = sorted([
    (n["repository"]["nameWithOwner"], n["number"], n["state"],
     n.get("mergedAt") or n.get("closedAt") or n.get("updatedAt") or "")
    for n in bot_prs
])
h = hashlib.sha256(json.dumps(key_tuples, sort_keys=True).encode()).hexdigest()[:16]
print()
print("trigger-set-hash:", h)
print("trigger-tuples:", key_tuples)
print("category-tuple:", (len(recent_merges), len(stale_open), len(closed_no_merge), len(active_open)))

# save summary
summary = {
    "today": "2026-07-16",
    "now": NOW.isoformat(),
    "bot_prs": len(bot_prs),
    "recent_merges": recent_merges,
    "stale_open": stale_open,
    "active_open": active_open,
    "closed_no_merge": closed_no_merge,
    "trigger_hash": h,
    "trigger_tuples": key_tuples,
    "category_tuple": [len(recent_merges), len(stale_open), len(closed_no_merge), len(active_open)],
}
import pathlib
pathlib.Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/summary.json").write_text(json.dumps(summary, indent=2, default=str))
