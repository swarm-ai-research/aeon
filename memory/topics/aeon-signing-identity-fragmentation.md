# Aeon signing-identity fragmentation

Aeon's bot account signs commits under a growing set of email identities that rotate by PR class rather than by repo or host. Every discovery has forced a per-run widening of the pr-tracker filter and reset the "still-missing patch" clock. This MOC centralises the domain-match filter argument and the rotation hypothesis.

## Observations (in discovery order)
- `aeonframework@users.noreply.github.com` — canonical noreply, dep-bump cluster (Agent-Reach#436, kage#66, InsForge#1742, openinterpreter#1810, wigolo#216, cocoindex#2315, RuView#1409, voicebox#958)
- `aeon@aeonframework.dev` — early direct-domain identity (Vibe-Trading#390, buzz#2248)
- [[aeon-third-signing-identity-proton-me]] — 2026-07-23, worldmonitor#5477, `fix/security/*` prefix
- [[aeon-fourth-signing-identity-security-aeonframework-dev]] — 2026-07-24, worldmonitor#5518, `security/bump-tauri-*`
- [[aeon-fifth-signing-identity-security-aeonframework-github]] — 2026-07-25, katanemo/plano#1001, `security/bump-dep-advisories-*`

## Durable claims
- [[aeon-bot-uses-multiple-signing-identities]] — parent lesson: any single-value `BOT_EMAIL` filter silently drops PRs
- [[aeon-bot-rotates-sender-by-pr-class]] — rotation is by PR class, not by repo or host
- [[pr-tracker-email-filter-must-be-domain-match]] — filter shape: `@aeonframework.*` plus noreply, not a fixed N-string OR list
- [[pr-tracker-branch-prefix-misses-bot-identity]] — the branch-prefix arm alone drops security/aeon/fix branches
- [[pr-tracker-branch-prefix-aeon-slash]] — 2026-07-24 discovery of a fifth branch prefix `aeon/*` on RuView#1409

## Contingent (may collapse)
- [[aeonframework-github-tld-is-google-delegation]] — `.github` sender may be a typo or one-off alias; watch next same-class PR to confirm or refute
