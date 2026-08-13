#!/usr/bin/env python3
"""Fetch PRs authored by aeonframework via gh graphql and write to graphql.json."""
import json
import subprocess
import sys
from pathlib import Path

QUERY = """
{
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
        repository { nameWithOwner isArchived }
        author { login }
        reviews(last: 1) { nodes { state submittedAt author { login } } }
        comments(last: 3) { totalCount nodes { createdAt author { login } bodyText } }
        commits(last: 1) { nodes { commit { author { email } } } }
      }
    }
  }
}
"""

def main():
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={QUERY}"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        print("GRAPHQL_ERR", result.returncode, result.stderr, file=sys.stderr)
        sys.exit(1)
    out = Path(__file__).parent / "graphql.json"
    out.write_text(result.stdout)
    data = json.loads(result.stdout)
    issue_count = data["data"]["search"]["issueCount"]
    nodes = data["data"]["search"]["nodes"]
    # Also filter for bot-branch PRs per memory (four prefixes: ai/, security/, fix/security/, aeon/)
    prefixes = ("ai/", "security/", "fix/security/", "aeon/")
    bot_prs = [n for n in nodes if (n.get("headRefName") or "").startswith(prefixes)]
    print(f"issueCount={issue_count} nodes={len(nodes)} botPRs={len(bot_prs)}")
    # State distribution of bot PRs
    from collections import Counter
    state_count = Counter(n["state"] for n in bot_prs)
    print(f"state_count={dict(state_count)}")

if __name__ == "__main__":
    main()
