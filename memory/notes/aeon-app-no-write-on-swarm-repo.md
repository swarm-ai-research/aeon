---
id: aeon-app-no-write-on-swarm-repo
created: 2026-06-20
type: project
links: [[github-actions-cannot-create-prs]]
---
# The aeon GitHub App token has no write access to `swarm-ai-research/swarm`

`pr-triage` and `pr-review` runs against that repo produce verdicts but `gh api .../labels`, `gh pr review`, `gh pr comment`, and the `addComment`/`addLabelsToLabelable` GraphQL mutations all return 403 "Resource not accessible by integration". Until the App is granted write scope, verdicts only land in the activity log and notify channels; `memory/triaged-prs.json` is intentionally left un-updated so a future run retries.
