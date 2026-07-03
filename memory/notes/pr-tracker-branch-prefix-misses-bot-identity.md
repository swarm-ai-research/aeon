---
id: pr-tracker-branch-prefix-misses-bot-identity
created: 2026-06-27
updated: 2026-07-03
type: lesson
links: [[gh-search-prs-api-drift]]
---
# Filtering bot PRs by branch-prefix misses non-`ai/` paths from the same author identity

`pr-tracker` filters bot PRs by the `ai/` branch prefix, but `Panniantong/Agent-Reach#436` (2026-06-26, branch `security/bump-vulnerable-deps`, commit author `aeonframework@users.noreply.github.com`) shows the same author identity can open PRs on other prefixes — likely `vuln-scanner` / dependabot-style auto-PRs — and the prefix filter drops them silently. Identity is stickier than branch convention: switching the filter to `BOT_EMAIL=aeonframework@users.noreply.github.com` (commit-author email) catches every aeon-authored bot path, including future prefixes. Until SKILL.md is patched, the GraphQL author-count diverges from the post-filter count and the operator never sees the real PRs.

**2026-07-03 update — a single BOT_EMAIL is not enough either.** `HKUDS/Vibe-Trading#390` opened today with commit author `aeon@aeonframework.dev` — a second aeon identity, different from the `aeonframework@users.noreply.github.com` used by every prior bot PR. Same author account, same `fix(deps): bump …` PR pattern, same `security/bump-*` branch convention — clearly the same bot process, just a different signing identity. So the durable SKILL.md fix must widen `BOT_EMAIL` from a single address to a **list or domain match** (e.g. any address whose domain is `aeonframework.dev` OR is the noreply address). Otherwise every new signing identity silently drops the corresponding bot PRs.
