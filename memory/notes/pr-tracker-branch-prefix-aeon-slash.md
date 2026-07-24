---
id: pr-tracker-branch-prefix-aeon-slash
created: 2026-07-24
type: observation
links: [[pr-tracker-branch-prefix-misses-bot-identity]], [[aeon-bot-uses-multiple-signing-identities]], [[pr-status]]
---
# A fifth aeon-bot branch prefix `aeon/*` appeared 2026-07-24 on `ruvnet/RuView#1409` — not startswith any of the current `ai/` / `security/` / `fix/security/` OR-filter entries

`ruvnet/RuView#1409` (fix(deps) fastapi + python-multipart, 7 HIGH CVEs) landed 2026-07-23T23:41:02Z with head branch `aeon/dep-bump-ruview-2026-07-23` — a novel `aeon/*` prefix that does not startswith any current OR-filter entry (`ai/`, `security/`, `fix/security/`). Inclusion held only because the email arm caught it (`aeonframework@users.noreply.github.com`); the branch-prefix arm alone would have silently dropped it. If the bot standardizes on `aeon/*` for more repos, the branch-prefix arm needs a fourth entry OR pr-tracker should stop maintaining branch-prefix state and rely only on the identity/email OR-list. Adds to the pr-tracker SKILL.md patch scope: FOUR signing identities × at least FOUR branch prefixes.
