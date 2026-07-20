#!/usr/bin/env python3
"""Fetch PRs authored by aeonframework via gh api graphql; write to prs.json."""
import subprocess
import json
import pathlib

query = '''
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
    ["gh", "api", "graphql", "-f", f"query={query}"],
    capture_output=True, text=True, check=False
)
out = pathlib.Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/prs.json")
out.write_text(result.stdout)
err = pathlib.Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/prs.err")
err.write_text(result.stderr)
print(f"rc={result.returncode}")
print(f"stdout bytes={len(result.stdout)}")
print(f"stderr bytes={len(result.stderr)}")
