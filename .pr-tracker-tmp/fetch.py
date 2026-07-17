#!/usr/bin/env python3
"""Fetch aeon-authored PRs via gh api graphql, categorize, and emit outputs."""
import json
import subprocess
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path

AUTHOR = "aeonframework"
BRANCH_PREFIX = "ai/"
# Multiple identities per [[aeon-bot-uses-multiple-signing-identities]]
KNOWN_BOT_EMAILS = {
    "aeonframework@users.noreply.github.com",
    "aeon@aeonframework.dev",
    # also allow bot-branch prefixes like security/*, ai/*, fix/*, feat/*, chore/*
}
KNOWN_BOT_BRANCH_PREFIXES = ("ai/", "security/", "fix/deps", "chore/deps")

TODAY = "2026-07-17"
NOW = datetime(2026, 7, 17, 10, 0, 0, tzinfo=timezone.utc)

query = """
{
  search(query: "author:%s is:pr sort:updated-desc", type: ISSUE, first: 60) {
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
}
""" % AUTHOR

result = subprocess.run(
    ["gh", "api", "graphql", "-f", "query=" + query],
    capture_output=True, text=True
)
rc = result.returncode
stderr = result.stderr
stdout = result.stdout
Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/rc.txt").write_text(str(rc) + "\n")
Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/stderr.txt").write_text(stderr)
Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/raw.json").write_text(stdout)
print(f"rc={rc} bytes={len(stdout)}")
if rc != 0:
    print("stderr:", stderr)
    sys.exit(1)

data = json.loads(stdout)
nodes = data.get("data", {}).get("search", {}).get("nodes", [])
print(f"total nodes: {len(nodes)}")

def is_bot_pr(node):
    head = node.get("headRefName", "") or ""
    email = ""
    commits = node.get("commits", {}).get("nodes", [])
    if commits:
        email = commits[0].get("commit", {}).get("author", {}).get("email", "") or ""
    if any(head.startswith(p) for p in KNOWN_BOT_BRANCH_PREFIXES):
        return True
    if email in KNOWN_BOT_EMAILS:
        return True
    return False

bot_prs = [n for n in nodes if is_bot_pr(n)]
print(f"bot PRs after filter: {len(bot_prs)}")

def parse_iso(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def days_ago(iso):
    dt = parse_iso(iso)
    if not dt:
        return None
    return (NOW - dt).total_seconds() / 86400.0

recent_merges = []
stale_open = []
active_open = []
closed_no_merge = []

for pr in bot_prs:
    state = pr.get("state")
    created = pr.get("createdAt")
    merged = pr.get("mergedAt")
    closed = pr.get("closedAt")
    updated = pr.get("updatedAt")
    repo = pr["repository"]["nameWithOwner"]
    number = pr["number"]
    title = pr["title"]

    d_created = days_ago(created)
    d_merged = days_ago(merged) if merged else None
    d_closed = days_ago(closed) if closed else None
    d_updated = days_ago(updated) if updated else None

    entry = {
        "repo": repo, "number": number, "title": title,
        "state": state, "url": pr["url"],
        "created": created, "merged": merged, "closed": closed, "updated": updated,
        "head": pr.get("headRefName"),
        "d_created": d_created, "d_merged": d_merged, "d_closed": d_closed, "d_updated": d_updated,
    }

    if state == "MERGED" and d_merged is not None and d_merged <= 7.0:
        recent_merges.append(entry)
    elif state == "OPEN":
        # stale = createdAt > 7d ago and no activity in last 7 days
        if d_created is not None and d_created > 7.0 and (d_updated is None or d_updated > 7.0):
            stale_open.append(entry)
        else:
            active_open.append(entry)
    elif state == "CLOSED" and d_closed is not None and d_closed <= 7.0:
        closed_no_merge.append(entry)

# Build trigger tuple (sorted for stable hash) — use raw node fields
triggers = sorted([
    (p["repository"]["nameWithOwner"], p["number"], p["state"],
     p.get("mergedAt") or p.get("closedAt") or p.get("updatedAt") or p.get("createdAt"))
    for p in bot_prs
])
trigger_str = json.dumps(triggers, sort_keys=True)
trigger_hash = hashlib.sha256(trigger_str.encode()).hexdigest()[:16]

category_tuple = (len(recent_merges), len(stale_open), len(closed_no_merge), len(active_open))

summary = {
    "today": TODAY,
    "author": AUTHOR,
    "total_bot_prs": len(bot_prs),
    "recent_merges": recent_merges,
    "stale_open": stale_open,
    "active_open": active_open,
    "closed_no_merge": closed_no_merge,
    "trigger_hash": trigger_hash,
    "category_tuple": list(category_tuple),
}
Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/summary.json").write_text(json.dumps(summary, indent=2))
print("category tuple:", category_tuple)
print("trigger hash:", trigger_hash)
print("bot PRs:")
for p in bot_prs:
    print(f"  - {p['repository']['nameWithOwner']}#{p['number']} state={p['state']} head={p.get('headRefName')} updated={p.get('updatedAt')}")
