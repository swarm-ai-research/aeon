---
id: org-cla-blocks-aeonframework-prs
created: 2026-08-30
type: lesson
links: [[cloudflare-org-cla-blocks-aeonframework-prs]], [[org-cla-block-resolution-splits-maintainer-vs-self]], [[pr-tracker-step-5-misses-fresh-bot-prs]], [[maintainer-close-without-merge-triage-pattern]]
---
# Cross-org CLA gates are the general class — cloudflare-org was the first instance, microsoft-org confirmed cross-org, browser-use is the third-member watch

Observed 2026-08-30: `microsoft/vscode#332891` (opened 08-27, self-closed 08-27 22:04Z ~14h after open with `CLAassistant` bot comment as the sole prior activity) confirms the cross-org widening flagged 08-27 — the block class is no longer cloudflare-specific. Members so far: `cloudflare.com` via [[cloudflare-org-cla-blocks-aeonframework-prs]] (Sub A maintainer-close ~6h), `microsoft.com` via vscode#332891 (Sub B operator self-close ~14h), and watch member `browser-use/browser-use#5564` (opened 08-27, `CLAassistant` bot 12s after open, ~2.7d unresolved at 08-30 scan). Consequence: any aeonframework submission to a repo whose org enforces a CLA-assistant bot replays the block cycle until either an org-scoped signature lands or the submitter self-closes; scanner skills (`vuln-scanner`, `external-feature`) that fan out CVE-bumps across arbitrary popular repos need an org-CLA-policy pre-flight or they'll keep burning close-cycles on every new org they touch.
