#!/bin/bash
set -e
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
        reviews(last: 3) { nodes { state submittedAt author { login } } }
        comments(last: 5) { totalCount nodes { author { login } createdAt body } }
        commits(last: 1) { nodes { commit { author { email } } } }
      }
    }
  }
}
' > /home/runner/work/aeon/aeon/.prt-scratch/graphql.json
echo "graphql-fetch-ok bytes=$(wc -c < /home/runner/work/aeon/aeon/.prt-scratch/graphql.json)"
