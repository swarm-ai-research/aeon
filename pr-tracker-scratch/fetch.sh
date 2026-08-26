#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
gh api graphql --raw-field query='{ search(query: "author:aeonframework is:pr sort:updated-desc", type: ISSUE, first: 60) { nodes { ... on PullRequest { number title state headRefName url createdAt updatedAt mergedAt closedAt repository { nameWithOwner isArchived } reviews(last: 1) { nodes { state submittedAt } } comments(last: 5) { totalCount nodes { author { login } createdAt } } commits(last: 1) { nodes { commit { author { email name } } } } } } } }' > raw.json
echo "Wrote raw.json"
jq '.data.search.nodes | length' raw.json
