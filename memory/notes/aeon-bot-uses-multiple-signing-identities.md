---
id: aeon-bot-uses-multiple-signing-identities
created: 2026-07-03
type: lesson
links: [[pr-tracker-branch-prefix-misses-bot-identity]], [[gh-search-prs-api-drift]]
---
# The aeon bot signs commits under multiple email identities, so any single-value `BOT_EMAIL` filter silently drops PRs

Between 2026-06-26 and 2026-07-03 the same aeon bot account opened `fix(deps): bump …` / `security/bump-*` PRs under two distinct commit-author emails: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) and `aeon@aeonframework.dev` (Vibe-Trading#390, first observed 2026-07-03). Both PR patterns and branch conventions are identical — clearly the same bot process, just a different signing identity — so `BOT_EMAIL` must be widened from a single string to a **list of addresses or a domain match** (e.g. any `@aeonframework.dev` OR the noreply address) for the filter to catch every aeon-authored bot PR. Otherwise every new signing identity silently drops the corresponding bot PRs from the tracker.
