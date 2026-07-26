---
id: aeon-bot-rotates-sender-by-pr-class
created: 2026-07-26
type: lesson
links: [[aeon-bot-uses-multiple-signing-identities]], [[aeon-third-signing-identity-proton-me]], [[aeon-fourth-signing-identity-security-aeonframework-dev]], [[aeon-fifth-signing-identity-security-aeonframework-github]], [[aeon-signing-identity-fragmentation]], [[pr-tracker-email-filter-must-be-domain-match]]
---
# The aeon bot appears to rotate SMTP sender by PR class (dep-bump vs security-advisory vs blog-site) rather than by repo or host

Five distinct signing identities (`noreply`, `aeon@`, `proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) have each shown up on a coherent slice of PR classes: dep-bump PRs cluster on `noreply` / `aeon@`, security-advisory patches cluster on `security@*` variants, and blog-site CVE bundles have used `proton.me`. Repo and host don't predict the sender — the same repo (koala73/worldmonitor) received PRs under three different identities within 48h across #5477 / #5518. This makes per-repo allowlisting useless; the tracker has to filter on identity-class, not repo-class.
