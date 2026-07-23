---
id: aeon-third-signing-identity-proton-me
created: 2026-07-23
type: observation
links: [[aeon-bot-uses-multiple-signing-identities]], [[pr-tracker-branch-prefix-misses-bot-identity]], [[pr-status]]
---
# A third aeon-bot signing identity `aeonframework@proton.me` appeared 2026-07-23 on `koala73/worldmonitor#5477` using a novel `fix/security/*` branch prefix

Prior known aeon-bot signing identities: `aeonframework@users.noreply.github.com` and `aeon@aeonframework.dev`. On 2026-07-23T08:11:57Z the aeon-authored PR `koala73/worldmonitor#5477` (sharp libvips CVE bundle) landed with commit-author `aeonframework@proton.me` on branch `fix/security/sharp-cve-blog-site` — both novel. Author.login is `aeonframework`, `is_bot: false`, and the patch shape (dep bump + lockfile regen + explicit CVE list in the body) matches the established CVE-tracking family, so this is real bot work. Any pr-tracker filter that hasn't widened its `BOT_EMAIL` list AND its branch-prefix list would silently drop it — pr-status.md's OR filter was widened on the run that discovered it. The pr-tracker SKILL.md patch backlog (27d overdue as of 2026-07-23) now needs to cover **three** identities and **at least three** branch prefixes (`ai/`, `security/`, `fix/security/`), not two.