---
id: graphql-statereason-only-on-issue-type
created: 2026-07-05
type: lesson
links: [[gh-search-prs-api-drift]]
---
# GitHub GraphQL `stateReason` field is on `Issue`, not `PullRequest`

`pr-tracker` SKILL.md ships a GraphQL query that requests `stateReason` on `PullRequest` nodes; the first invocation on 2026-07-05 hard-failed with `Field 'stateReason' doesn't exist on type 'PullRequest'`. `stateReason` (COMPLETED / DUPLICATE / REOPENED / NOT_PLANNED) is defined only on `Issue`; for PRs use `state` (OPEN / CLOSED / MERGED) plus `mergedAt` presence to derive closed-no-merge. Same drift class as `headRefName` / `mergedAt` / `--state merged` in [[gh-search-prs-api-drift]] — batch these into a single SKILL.md patch.
