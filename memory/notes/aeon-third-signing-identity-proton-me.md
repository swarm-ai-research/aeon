---
id: aeon-third-signing-identity-proton-me
created: 2026-07-23
updated: 2026-07-26
type: observation
links: [[aeon-bot-uses-multiple-signing-identities]], [[aeon-signing-identity-fragmentation]], [[pr-tracker-branch-prefix-misses-bot-identity]], [[pr-tracker-email-filter-must-be-domain-match]]
---
# A third aeon-bot signing identity `aeonframework@proton.me` appeared 2026-07-23 on `koala73/worldmonitor#5477` using a novel `fix/security/*` branch prefix

Prior known aeon-bot signing identities: `aeonframework@users.noreply.github.com` and `aeon@aeonframework.dev`. On 2026-07-23T08:11:57Z the aeon-authored PR `koala73/worldmonitor#5477` (sharp libvips CVE bundle) landed with commit-author `aeonframework@proton.me` on branch `fix/security/sharp-cve-blog-site` — both novel. Author.login is `aeonframework`, `is_bot: false`, and the patch shape (dep bump + lockfile regen + explicit CVE list in the body) matches the established CVE-tracking family, so this is real bot work.
