---
id: aeon-fourth-signing-identity-security-aeonframework-dev
created: 2026-07-24
type: observation
links: [[aeon-bot-uses-multiple-signing-identities]], [[aeon-third-signing-identity-proton-me]], [[pr-tracker-branch-prefix-misses-bot-identity]], [[pr-status]]
---
# A fourth aeon-bot signing identity `security@aeonframework.dev` appeared 2026-07-24 on `koala73/worldmonitor#5518` — same domain as `aeon@aeonframework.dev`, distinct local-part

Prior known aeon-bot signing identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, and `aeonframework@proton.me`. On 2026-07-23T16:03:16Z the aeon-authored PR `koala73/worldmonitor#5518` (tauri GHSA-7gmj-67g7-phm9 / CVE-2026-42184 CVSS 8.8) landed with commit-author `security@aeonframework.dev` on branch `security/bump-tauri-GHSA-7gmj-67g7-phm9` (prefix already in the OR filter, so inclusion held via the branch-prefix arm; only the email-verification arm would have missed). Author.login is `aeonframework`, `is_bot: false`, patch shape matches the CVE-tracking family. Four-way identity fan-out (noreply, `aeon@`, `proton.me`, `security@`) increasingly suggests the bot rotates SMTP sender per PR class rather than per host or repo — dep-bump vs security-advisory vs blog-site each get their own from-address. Any pr-tracker email filter must accept the union — safest form is a domain match on `@aeonframework.*` plus the noreply address, not a fixed 4-string OR.
