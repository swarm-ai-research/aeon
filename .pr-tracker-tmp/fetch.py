#!/usr/bin/env python3
"""pr-tracker fetch: GraphQL primary, gh search fallback."""
import subprocess, json, sys, pathlib

out = pathlib.Path(".pr-tracker-tmp")
out.mkdir(parents=True, exist_ok=True)

QUERY = '''{
  search(query: "author:aeonframework is:pr sort:updated-desc", type: ISSUE, first: 60) {
    nodes {
      ... on PullRequest {
        number
        title
        state
        headRefName
        url
        createdAt
        mergedAt
        closedAt
        updatedAt
        repository { nameWithOwner }
        reviews(last: 1) { nodes { state submittedAt } }
        comments { totalCount }
        commits(last: 1) { nodes { commit { author { email } } } }
      }
    }
  }
}'''

r = subprocess.run(
    ["gh", "api", "graphql", "-f", f"query={QUERY}"],
    capture_output=True, text=True
)
(out / "raw.json").write_text(r.stdout)
(out / "raw.err").write_text(r.stderr)
print(f"rc={r.returncode} stdout_bytes={len(r.stdout)} stderr_bytes={len(r.stderr)}")

if r.returncode != 0:
    print("FALLBACK NEEDED", file=sys.stderr)
    sys.exit(2)

data = json.loads(r.stdout)
nodes = data.get("data", {}).get("search", {}).get("nodes", [])
print(f"nodes={len(nodes)}")
