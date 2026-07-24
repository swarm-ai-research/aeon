#!/bin/bash
set -e
AUTHOR="aeonframework"
gh api graphql -f query='
{
  search(query: "author:'"$AUTHOR"' is:pr sort:updated-desc", type: ISSUE, first: 60) {
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
        reviews(last: 3) { nodes { state submittedAt } }
        comments { totalCount }
        commits(last: 1) { nodes { commit { author { email } } } }
      }
    }
  }
}' > raw.json
echo "rc=$?"
jq '.data.search.nodes | length' raw.json
