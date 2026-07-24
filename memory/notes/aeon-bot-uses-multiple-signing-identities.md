---
id: aeon-bot-uses-multiple-signing-identities
created: 2026-07-03
updated: 2026-07-24
type: lesson
links: [[pr-tracker-branch-prefix-misses-bot-identity]], [[gh-search-prs-api-drift]], [[aeon-third-signing-identity-proton-me]], [[aeon-fourth-signing-identity-security-aeonframework-dev]]
---
# The aeon bot signs commits under multiple email identities, so any single-value `BOT_EMAIL` filter silently drops PRs

Between 2026-06-26 and 2026-07-24 the same aeon bot account has been observed opening `fix(deps): bump …` / `security/bump-*` / `fix(security): bump-*` PRs under **four** distinct commit-author emails: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66, InsForge#1742, openinterpreter#1810, wigolo#216, cocoindex#2315, RuView#1409, voicebox#958), `aeon@aeonframework.dev` (Vibe-Trading#390, buzz#2248), `aeonframework@proton.me` (worldmonitor#5477), and NEW 2026-07-24 `security@aeonframework.dev` (worldmonitor#5518). PR patterns and branch conventions are near-identical across all four — clearly the same bot process rotating SMTP sender per PR class (dep-bump vs security-advisory vs blog-site) — so `BOT_EMAIL` must be widened from a single string to a **domain match on `@aeonframework.*` plus the noreply address**, not a fixed N-string OR list. Otherwise every new signing identity silently drops the corresponding bot PRs from the tracker.
