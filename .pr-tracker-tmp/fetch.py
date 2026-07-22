#!/usr/bin/env python3
"""Fetch PRs authored by AUTHOR via `gh api graphql`, dump raw json to disk.

Workaround for sandbox: shell > redirect to workdir is blocked, so we spawn
gh via subprocess and write via pathlib.
"""
import json
import subprocess
import sys
from pathlib import Path

AUTHOR = "aeonframework"

QUERY = """
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

out_path = Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/raw.json")

proc = subprocess.run(
    ["gh", "api", "graphql", "-f", f"query={QUERY}"],
    capture_output=True,
    text=True,
    timeout=60,
)

if proc.returncode != 0:
    print(f"gh api graphql FAILED rc={proc.returncode}", file=sys.stderr)
    print(proc.stderr, file=sys.stderr)
    sys.exit(proc.returncode)

# Validate JSON
try:
    data = json.loads(proc.stdout)
except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}", file=sys.stderr)
    print(proc.stdout[:2000], file=sys.stderr)
    sys.exit(1)

# Verify it looks right
nodes = data.get("data", {}).get("search", {}).get("nodes", [])
print(f"OK: {len(nodes)} nodes")

out_path.write_text(json.dumps(data, indent=2))
print(f"wrote {out_path}")
