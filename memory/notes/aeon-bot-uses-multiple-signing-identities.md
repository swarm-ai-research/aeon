---
id: aeon-bot-uses-multiple-signing-identities
created: 2026-07-03
updated: 2026-07-23
type: lesson
links: [[pr-tracker-branch-prefix-misses-bot-identity]], [[gh-search-prs-api-drift]], [[aeon-third-signing-identity-proton-me]]
---
# The aeon bot signs commits under multiple email identities, so any single-value `BOT_EMAIL` filter silently drops PRs

Between 2026-06-26 and 2026-07-23 the same aeon bot account has been observed opening `fix(deps): bump …` / `security/bump-*` / `fix(security): bump-*` PRs under **three** distinct commit-author emails: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66, InsForge#1742, openinterpreter#1810, wigolo#216, cocoindex#2315), `aeon@aeonframework.dev` (Vibe-Trading#390, buzz#2248), and NEW 2026-07-23 `aeonframework@proton.me` (worldmonitor#5477). PR patterns and branch conventions are near-identical across all three — clearly the same bot process, just a different signing identity — so `BOT_EMAIL` must be widened from a single string to a **list of addresses or a domain match** (e.g. any `@aeonframework.*` OR the noreply address) for the filter to catch every aeon-authored bot PR. Otherwise every new signing identity silently drops the corresponding bot PRs from the tracker.
