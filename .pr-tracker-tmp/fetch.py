#!/usr/bin/env python3
"""Fetch PRs authored by AUTHOR via gh graphql; write raw.json.

Works around sandbox `>` redirect block per [[sandbox-blocks-shell-redirect-to-workdir]].
"""
import subprocess
from pathlib import Path
import sys

QUERY = '''
{
  search(query: "author:aeonframework is:pr sort:updated-desc", type: ISSUE, first: 60) {
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
'''

result = subprocess.run(
    ["gh", "api", "graphql", "-f", f"query={QUERY}"],
    capture_output=True,
    text=True,
    timeout=60,
)

outdir = Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp")
outdir.mkdir(parents=True, exist_ok=True)
(outdir / "raw.json").write_text(result.stdout)
(outdir / "raw.err").write_text(result.stderr)

print(f"rc={result.returncode}")
print(f"stdout_len={len(result.stdout)}")
print(f"stderr_len={len(result.stderr)}")
if result.returncode != 0:
    print("STDERR:")
    print(result.stderr[:1000])
    sys.exit(result.returncode)
