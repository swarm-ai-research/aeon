---
id: gh-search-prs-drops-headrefname-field
created: 2026-06-23
type: lesson
links: [[gh-search-prs-drops-state-merged-flag]], [[gh-search-prs-drops-mergedat-field]], [[pr-tracker-branch-prefix-aeon-slash]]
---
# `gh search prs --json headRefName` no longer resolves — filter by branch via the GraphQL primary

The current `gh` CLI no longer exposes `headRefName` in `--json` output for `gh search prs`; queries requesting it fail with a field-unknown error. Skills that filtered PRs by branch prefix via this field must switch to `gh api graphql` on `search { nodes { ... on PullRequest { headRefName } } }`, or fall back to `gh pr list -R $repo --json headRefName` after resolving the repo separately. First hit 2026-06-23 alongside the `--state merged` drift.
