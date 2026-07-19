#!/usr/bin/env python3
"""Fetch PRs authored by aeonframework via gh graphql, write to JSON."""
import json
import subprocess
import sys
from pathlib import Path

AUTHOR = "aeonframework"

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

out = subprocess.run(
    ["gh", "api", "graphql", "-f", "query=" + query],
    capture_output=True, text=True
)

if out.returncode != 0:
    sys.stderr.write("gh graphql failed rc=%d\n" % out.returncode)
    sys.stderr.write(out.stderr)
    sys.exit(out.returncode)

data = json.loads(out.stdout)
nodes = data.get("data", {}).get("search", {}).get("nodes", [])

# Filter: keep bot PRs — branch startswith ai/ or security/, OR commit-author email is known bot identity.
KNOWN_BOT_EMAILS = {
    "aeonframework@users.noreply.github.com",
    "aeon@aeonframework.dev",
}
KNOWN_PREFIXES = ("ai/", "security/")

kept = []
for n in nodes:
    if not n:
        continue
    branch = n.get("headRefName") or ""
    email = ""
    try:
        email = (n.get("commits", {}).get("nodes") or [{}])[0].get("commit", {}).get("author", {}).get("email") or ""
    except Exception:
        email = ""
    if branch.startswith(KNOWN_PREFIXES) or email in KNOWN_BOT_EMAILS:
        n["_commitEmail"] = email
        kept.append(n)

Path(".pr-tracker-tmp/raw.json").write_text(json.dumps(nodes, indent=2))
Path(".pr-tracker-tmp/kept.json").write_text(json.dumps(kept, indent=2))

print("total_nodes=%d kept=%d" % (len(nodes), len(kept)))
for k in kept:
    print("  %s#%d %s branch=%s email=%s" % (
        k.get("repository", {}).get("nameWithOwner"),
        k.get("number"),
        k.get("state"),
        k.get("headRefName"),
        k.get("_commitEmail"),
    ))
