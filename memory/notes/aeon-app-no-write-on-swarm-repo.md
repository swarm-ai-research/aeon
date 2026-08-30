---
id: aeon-app-no-write-on-swarm-repo
created: 2026-06-20
type: project
links: [[github-actions-cannot-create-prs]]
---
# The aeon GitHub App token has no write access to `swarm-ai-research/swarm`

`pr-triage` and `pr-review` runs against that repo produce verdicts but `gh api .../labels`, `gh pr review`, `gh pr comment`, and the `addComment`/`addLabelsToLabelable` GraphQL mutations all return 403 "Resource not accessible by integration". Class hypothesis promoted **suspected → confirmed** 2026-08-29 during the 65th `pr-review` invocation (first non-full-skip after a 20-run streak): a 3-day gap since the 64th run opened a window past SKILL's 2-day dup-SHA guard, so step-7 attempted writes on human PRs #549/#543 and both `POST /repos/.../pulls/549/comments` and `gh pr review --comment` returned the 403 payload verbatim. Until the App is granted `pull_requests: write` (or the skill is routed via a PAT-backed path, or documented as report-only for swarm), verdicts only land in the activity log and notify channels; `memory/triaged-prs.json` is intentionally left un-updated so a future run retries.
