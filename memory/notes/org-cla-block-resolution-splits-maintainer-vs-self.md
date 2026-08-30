---
id: org-cla-block-resolution-splits-maintainer-vs-self
created: 2026-08-30
type: lesson
links: [[org-cla-blocks-aeonframework-prs]], [[cloudflare-org-cla-blocks-aeonframework-prs]], [[pr-tracker-stale-bot-comment-inverts-stale-classification]]
---
# CLA-block PRs resolve two ways depending on who acts first: maintainer-close (~6h, formal) vs operator self-close (~14h, retreat after CLAassistant bot posts)

The two confirmed CLA-block instances resolved through different actors: `cloudflare/workerd#7124` was closed 2026-08-26 05:30Z by maintainer `ryanking13` ~6h after the CLAassistant bot demanded a signature (**Sub A: maintainer-close**), while `microsoft/vscode#332891` was closed by `aeonframework` itself 2026-08-27 22:04:40Z ~14h after the same bot pattern (**Sub B: operator self-close**, comment at 22:04:39Z → close at 22:04:40Z, 1s delta implies scripted retreat). Predictor implication: CLA-block PRs are not a single close-cadence bucket — Sub A closes fast and shows up in `closed7d` within one scan cycle, Sub B closes on a lag governed by the operator's own retry logic; `pr-tracker` SKILL patch item (m) needs to split the CLA-block bucket by close-actor to keep the tuple predictor from missing the slower Sub B resolutions.
