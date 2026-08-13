#!/usr/bin/env bash
set -euo pipefail
OUT="$(dirname "$0")/graphql.json"
gh api graphql -f query='
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
}' > "$OUT"
echo "written: $OUT"
jq '.data.search.issueCount, (.data.search.nodes | length)' "$OUT"
