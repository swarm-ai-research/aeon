---
id: aeon-bot-uses-multiple-signing-identities
created: 2026-07-03
updated: 2026-07-26
type: lesson
links: [[aeon-signing-identity-fragmentation]], [[aeon-bot-rotates-sender-by-pr-class]], [[pr-tracker-email-filter-must-be-domain-match]], [[pr-tracker-branch-prefix-misses-bot-identity]], [[gh-search-prs-api-drift]]
---
# The aeon bot signs commits under multiple email identities, so any single-value `BOT_EMAIL` filter silently drops PRs

Between 2026-06-26 and 2026-07-25 the same aeon bot account has been observed opening `fix(deps): bump …` / `security/bump-*` / `fix(security): bump-*` PRs under **five** distinct commit-author emails — see [[aeon-signing-identity-fragmentation]] for the full fan-out. `BOT_EMAIL` must therefore be a domain match, not a fixed N-string OR list, per [[pr-tracker-email-filter-must-be-domain-match]].
