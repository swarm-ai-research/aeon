#!/usr/bin/env python3
"""pr-tracker analyze — categorize + compute canonical hash."""
import json
import subprocess
import hashlib
from datetime import datetime, timezone
from pathlib import Path

TMP = Path(__file__).parent
NOW = datetime(2026, 7, 24, 11, 28, 10, tzinfo=timezone.utc)

# Fetch fresh
raw = subprocess.run(
    ["gh", "api", "graphql", "-f", "query=" + """
{
  search(query: "author:aeonframework is:pr sort:updated-desc", type: ISSUE, first: 60) {
    nodes {
      ... on PullRequest {
        number title state headRefName url createdAt updatedAt mergedAt closedAt
        repository { nameWithOwner }
        reviews(last: 3) { nodes { state submittedAt } }
        comments { totalCount }
        commits(last: 1) { nodes { commit { author { email } } } }
      }
    }
  }
}"""],
    check=True, capture_output=True, text=True
)
data = json.loads(raw.stdout)
nodes = data["data"]["search"]["nodes"]
(TMP / "raw.json").write_text(json.dumps(data, indent=2))
print(f"nodes={len(nodes)}")

# OR-filter — three branch prefixes OR four known bot emails
PREFIXES = ("ai/", "security/", "fix/security/")
EMAILS = {
    "aeonframework@users.noreply.github.com",
    "aeon@aeonframework.dev",
    "aeonframework@proton.me",
    "security@aeonframework.dev",
}

def is_bot(n):
    br = n.get("headRefName", "") or ""
    em = ""
    try:
        em = n["commits"]["nodes"][0]["commit"]["author"]["email"] or ""
    except Exception:
        pass
    return any(br.startswith(p) for p in PREFIXES) or em in EMAILS

bot_nodes = [n for n in nodes if is_bot(n)]
print(f"bot_nodes={len(bot_nodes)}")

# Emit filter breakdown
for n in bot_nodes:
    email = n["commits"]["nodes"][0]["commit"]["author"]["email"]
    print(f"  {n['repository']['nameWithOwner']}#{n['number']} state={n['state']} branch={n['headRefName']} email={email}")

def parse(dt):
    if not dt: return None
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

def days_ago(dt):
    if not dt: return None
    return (NOW - parse(dt)).total_seconds() / 86400

# Categorize
merged_7d = []
stale_open = []
active_open = []
closed_no_merge_7d = []
open_all = []

for n in bot_nodes:
    st = n["state"]
    created_age = days_ago(n["createdAt"])
    updated_age = days_ago(n["updatedAt"])
    if st == "MERGED":
        m_age = days_ago(n["mergedAt"])
        if m_age is not None and m_age <= 7:
            merged_7d.append(n)
    elif st == "CLOSED":
        c_age = days_ago(n["closedAt"])
        if c_age is not None and c_age <= 7:
            closed_no_merge_7d.append(n)
    elif st == "OPEN":
        open_all.append(n)
        # stale: >7d old AND no activity in last 7d
        if created_age > 7 and updated_age > 7:
            stale_open.append(n)
        else:
            active_open.append(n)

print(f"\nBUCKETS:")
print(f"  merged_7d={len(merged_7d)}")
print(f"  stale_open={len(stale_open)}")
print(f"  active_open={len(active_open)}")
print(f"  closed_no_merge_7d={len(closed_no_merge_7d)}")
print(f"  open_all={len(open_all)}")

# Canonical hash — same recipe as yesterday
tuples = sorted([
    f"{n['repository']['nameWithOwner']}#{n['number']}:{n['state']}:{n['updatedAt']}"
    for n in bot_nodes
])
canon = "|".join(tuples)
h = hashlib.sha256(canon.encode()).hexdigest()[:16]
print(f"\nhash={h}")
print(f"yesterday_hash=85ca269f4eb6c567 (from memory)")

# Also compute fresh-bot-PR trigger
fresh = [n for n in bot_nodes if n["state"] == "OPEN" and days_ago(n["createdAt"]) < 1]
print(f"fresh_bot_prs (<24h): {len(fresh)}")
for f in fresh:
    age_h = days_ago(f["createdAt"]) * 24
    print(f"  {f['repository']['nameWithOwner']}#{f['number']} ({age_h:.1f}h)")

# Dump categorized data
result = {
    "now": NOW.isoformat().replace("+00:00", "Z"),
    "hash": h,
    "prev_hash": "85ca269f4eb6c567",
    "buckets": {
        "merged_7d": [{"repo": n["repository"]["nameWithOwner"], "num": n["number"], "title": n["title"], "url": n["url"], "created": n["createdAt"], "merged": n.get("mergedAt")} for n in merged_7d],
        "stale_open": [{"repo": n["repository"]["nameWithOwner"], "num": n["number"], "title": n["title"], "url": n["url"], "created": n["createdAt"], "updated": n["updatedAt"], "age_d": round(days_ago(n["createdAt"]), 2), "quiet_d": round(days_ago(n["updatedAt"]), 2)} for n in stale_open],
        "active_open": [{"repo": n["repository"]["nameWithOwner"], "num": n["number"], "title": n["title"], "url": n["url"], "created": n["createdAt"], "updated": n["updatedAt"], "age_d": round(days_ago(n["createdAt"]), 2), "quiet_d": round(days_ago(n["updatedAt"]), 2), "comments": n["comments"]["totalCount"], "reviews": n["reviews"]["nodes"], "email": n["commits"]["nodes"][0]["commit"]["author"]["email"], "branch": n["headRefName"]} for n in active_open],
        "closed_no_merge_7d": [{"repo": n["repository"]["nameWithOwner"], "num": n["number"], "title": n["title"], "url": n["url"], "closed": n["closedAt"]} for n in closed_no_merge_7d],
    },
    "counts": {
        "merged_7d": len(merged_7d),
        "stale_open": len(stale_open),
        "active_open": len(active_open),
        "closed_no_merge_7d": len(closed_no_merge_7d),
        "open_total": len(open_all),
        "fresh_bot_prs": len(fresh),
    },
    "fresh_bot_prs": [{"repo": n["repository"]["nameWithOwner"], "num": n["number"], "age_h": round(days_ago(n["createdAt"]) * 24, 1)} for n in fresh],
}
(TMP / "result.json").write_text(json.dumps(result, indent=2))
print("\nwrote result.json")
