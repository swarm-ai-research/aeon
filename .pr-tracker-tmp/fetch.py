#!/usr/bin/env python3
"""Run gh graphql to enumerate PRs authored by AUTHOR; write JSON to stdout dump."""
import json
import subprocess
import pathlib
import sys

AUTHOR = "aeonframework"

QUERY = '''
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
''' % AUTHOR

result = subprocess.run(
    ["gh", "api", "graphql", "-f", f"query={QUERY}"],
    capture_output=True, text=True, timeout=60
)
if result.returncode != 0:
    sys.stderr.write(f"[FETCH_FAIL rc={result.returncode}]\n{result.stderr}\n")
    sys.exit(result.returncode)

pathlib.Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/raw.json").write_text(result.stdout)
data = json.loads(result.stdout)
nodes = data.get("data", {}).get("search", {}).get("nodes", []) or []
print(f"[FETCH_OK nodes={len(nodes)}]")
for n in nodes:
    print(f"  {n['repository']['nameWithOwner']}#{n['number']} [{n['state']}] head={n['headRefName']} updatedAt={n.get('updatedAt')}")
