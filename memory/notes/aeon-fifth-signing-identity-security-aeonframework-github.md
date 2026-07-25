---
id: aeon-fifth-signing-identity-security-aeonframework-github
created: 2026-07-25
type: observation
links: [[aeon-bot-uses-multiple-signing-identities]], [[aeon-fourth-signing-identity-security-aeonframework-dev]], [[aeon-third-signing-identity-proton-me]], [[pr-tracker-branch-prefix-misses-bot-identity]], [[pr-status]]
---
# A fifth aeon-bot signing identity `security@aeonframework.github` appeared 2026-07-25 on `katanemo/plano#1001` — same local part as the fourth identity, unusual `.github` TLD

Prior known aeon-bot signing identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, and `security@aeonframework.dev`. On 2026-07-24T15:27:20Z the aeon-authored PR `katanemo/plano#1001` (patches serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs) landed with commit-author `security@aeonframework.github` on branch `security/bump-dep-advisories-2026-07-24` (prefix already in the OR filter). The `.github` TLD is a real delegation (Google) but the domain `aeonframework.github` is not observably in wide public use — likely an internal alias or typo of `aeonframework.dev`. Five-way identity fan-out solidifies the "bot rotates SMTP sender per PR class rather than per repo" hypothesis; pr-tracker email arm must remain a domain match on `@aeonframework.*` plus the noreply address, not a fixed 5-string OR. Watch: if next same-class PR standardizes on `security@aeonframework.dev`, this is a one-off; if it repeats, `.github` is a real second production domain.
