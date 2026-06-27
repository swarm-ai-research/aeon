---
id: pr-tracker-branch-prefix-misses-bot-identity
created: 2026-06-27
type: lesson
links: [[gh-search-prs-api-drift]]
---
# Filtering bot PRs by branch-prefix misses non-`ai/` paths from the same author identity

`pr-tracker` filters bot PRs by the `ai/` branch prefix, but `Panniantong/Agent-Reach#436` (2026-06-26, branch `security/bump-vulnerable-deps`, commit author `aeonframework@users.noreply.github.com`) shows the same author identity can open PRs on other prefixes — likely `vuln-scanner` / dependabot-style auto-PRs — and the prefix filter drops them silently. Identity is stickier than branch convention: switching the filter to `BOT_EMAIL=aeonframework@users.noreply.github.com` (commit-author email) catches every aeon-authored bot path, including future prefixes. Until SKILL.md is patched, the GraphQL author-count diverges from the post-filter count and the operator never sees the real PRs.
