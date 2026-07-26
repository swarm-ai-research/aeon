#!/usr/bin/env python3
"""Fetch PRs authored by aeonframework via GraphQL, apply widened bot filter, dump JSON."""
import subprocess, json, sys, pathlib

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
}
'''

BRANCH_PREFIXES = ("ai/", "security/", "fix/security/", "aeon/")
BOT_EMAILS = {
    "aeonframework@users.noreply.github.com",
    "aeon@aeonframework.dev",
    "aeonframework@proton.me",
    "security@aeonframework.dev",
    "security@aeonframework.github",
}

def main():
    r = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={QUERY}"],
        capture_output=True, text=True, timeout=60,
    )
    if r.returncode != 0:
        print("ERR gh graphql:", r.stderr, file=sys.stderr)
        sys.exit(2)
    data = json.loads(r.stdout)
    nodes = data.get("data", {}).get("search", {}).get("nodes", []) or []
    kept = []
    for n in nodes:
        if not n:
            continue
        branch = n.get("headRefName") or ""
        commits = n.get("commits", {}).get("nodes") or []
        email = ""
        if commits:
            email = (commits[0].get("commit", {}).get("author") or {}).get("email") or ""
        branch_hit = any(branch.startswith(p) for p in BRANCH_PREFIXES)
        email_hit  = email in BOT_EMAILS
        if branch_hit or email_hit:
            n["_email"] = email
            n["_branch_hit"] = branch_hit
            n["_email_hit"] = email_hit
            kept.append(n)
    out = pathlib.Path(".pr-tracker-tmp/prs.json")
    out.write_text(json.dumps(kept, indent=2))
    print(f"total_nodes={len(nodes)} kept={len(kept)}")
    # summary
    for k in kept:
        repo = k["repository"]["nameWithOwner"]
        num  = k["number"]
        state = k["state"]
        branch = k["headRefName"]
        email = k.get("_email", "")
        print(f"  {repo}#{num} {state} branch={branch} email={email}")

if __name__ == "__main__":
    main()
