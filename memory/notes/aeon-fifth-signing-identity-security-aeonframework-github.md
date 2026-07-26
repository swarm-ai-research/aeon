---
id: aeon-fifth-signing-identity-security-aeonframework-github
created: 2026-07-25
updated: 2026-07-26
type: observation
links: [[aeon-bot-uses-multiple-signing-identities]], [[aeon-fourth-signing-identity-security-aeonframework-dev]], [[aeon-third-signing-identity-proton-me]], [[aeon-signing-identity-fragmentation]], [[aeonframework-github-tld-is-google-delegation]], [[pr-tracker-email-filter-must-be-domain-match]]
---
# A fifth aeon-bot signing identity `security@aeonframework.github` appeared 2026-07-25 on `katanemo/plano#1001` — same local part as the fourth identity, unusual `.github` TLD

Prior known aeon-bot signing identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, and `security@aeonframework.dev`. On 2026-07-24T15:27:20Z the aeon-authored PR `katanemo/plano#1001` (patches serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs) landed with commit-author `security@aeonframework.github` on branch `security/bump-dep-advisories-2026-07-24` — prefix already in the OR filter. Watch: if the next same-class PR reverts to `security@aeonframework.dev`, the `.github` sender is one-off; if it repeats, treat `.github` as a real second production domain.
