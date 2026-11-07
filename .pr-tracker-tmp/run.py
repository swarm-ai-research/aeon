#!/usr/bin/env python3
"""pr-tracker scan runner — fetches via gh GraphQL, categorizes, writes outputs."""
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

TODAY_STR = "2026-11-07"
TODAY = datetime(2026, 11, 7, tzinfo=timezone.utc)
AUTHOR = "aeonframework"
BRANCH_PREFIXES = ("ai/", "security/", "fix/security/", "aeon/", "fix/", "hook-submission/")
BOT_EMAIL = ""

QUERY = """{
  search(query: "author:aeonframework is:pr sort:updated-desc", type: ISSUE, first: 60) {
    issueCount
    nodes {
      ... on PullRequest {
        number
        title
        state
        headRefName
        url
        createdAt
        updatedAt
        mergedAt
        closedAt
        repository { nameWithOwner }
        reviews(last: 1) { nodes { state submittedAt } }
        comments { totalCount }
        commits(last: 1) { nodes { commit { author { email } } } }
      }
    }
  }
}"""

def fetch_graphql():
    for attempt in range(1, 5):
        proc = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={QUERY}"],
            capture_output=True, text=True,
        )
        out = proc.stdout
        err = proc.stderr
        if out:
            try:
                data = json.loads(out)
                if "data" in data and data["data"] and data["data"].get("search"):
                    return data, attempt, err
            except json.JSONDecodeError:
                pass
        if attempt < 4:
            import time
            time.sleep(3)
    return None, attempt, err

def parse_iso(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def main():
    data, attempts, err_txt = fetch_graphql()
    if data is None:
        print("GRAPHQL_FAIL", file=sys.stderr)
        print(err_txt, file=sys.stderr)
        sys.exit(2)

    search = data["data"]["search"]
    issue_count = search["issueCount"]
    nodes = search["nodes"] or []

    # separate null slots (empty dicts from IP-allowlist blocks)
    concrete = [n for n in nodes if n]
    null_slots = len(nodes) - len(concrete)

    # filter by branch prefix
    prefix_match = [n for n in concrete if n.get("headRefName", "").startswith(BRANCH_PREFIXES)]
    non_prefix = [n for n in concrete if not n.get("headRefName", "").startswith(BRANCH_PREFIXES)]

    seven_ago = TODAY - timedelta(days=7)
    thirty_ago = TODAY - timedelta(days=30)

    recent_merges = []  # state==MERGED, mergedAt within 7d
    stale_open = []     # OPEN, createdAt >7d ago, no review/comment activity in last 7d
    active_open = []    # OPEN, createdAt within 7d OR recent comment/review activity
    closed_nomerge = [] # state==CLOSED (not merged) & closedAt within 7d
    recent_merges_30 = []  # for 30d table
    closed_nomerge_30 = []

    all_open = []
    for n in prefix_match:
        state = n["state"]
        created = parse_iso(n["createdAt"])
        updated = parse_iso(n["updatedAt"])
        merged = parse_iso(n.get("mergedAt"))
        closed = parse_iso(n.get("closedAt"))
        if state == "MERGED":
            if merged and merged >= seven_ago:
                recent_merges.append(n)
            if merged and merged >= thirty_ago:
                recent_merges_30.append(n)
        elif state == "CLOSED":
            if closed and closed >= seven_ago:
                closed_nomerge.append(n)
            if closed and closed >= thirty_ago:
                closed_nomerge_30.append(n)
        elif state == "OPEN":
            all_open.append(n)
            # recent review or comment activity?
            recent_activity = False
            revs = n.get("reviews", {}).get("nodes", [])
            for r in revs:
                st = parse_iso(r.get("submittedAt"))
                if st and st >= seven_ago:
                    recent_activity = True
                    break
            if updated and updated >= seven_ago:
                recent_activity = True
            if created and created >= seven_ago:
                active_open.append(n)
            elif recent_activity:
                active_open.append(n)
            else:
                stale_open.append(n)

    buckets = {
        "merged7d": len(recent_merges),
        "staleOpen": len(stale_open),
        "closed7d": len(closed_nomerge),
        "activeOpen": len(active_open),
        "openTotal": len(all_open),
        "merged30d": len(recent_merges_30),
        "closed30d": len(closed_nomerge_30),
        "issueCount": issue_count,
        "nullSlots": null_slots,
        "nonPrefix": len(non_prefix),
        "prefixMatch": len(prefix_match),
    }

    out = {
        "attempts": attempts,
        "buckets": buckets,
        "recent_merges": recent_merges,
        "recent_merges_30": recent_merges_30,
        "stale_open": stale_open,
        "active_open": active_open,
        "closed_nomerge": closed_nomerge,
        "closed_nomerge_30": closed_nomerge_30,
        "all_open": all_open,
        "non_prefix": non_prefix,
        "prefix_match_count": len(prefix_match),
    }
    Path(".pr-tracker-tmp/result.json").write_text(json.dumps(out, indent=2, default=str))
    print(json.dumps(buckets, indent=2))

if __name__ == "__main__":
    main()
