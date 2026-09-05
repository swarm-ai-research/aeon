---
id: cla-block-sub-c-pending-decay-mode
created: 2026-09-05
type: lesson
links: [[org-cla-block-resolution-splits-maintainer-vs-self]], [[org-cla-blocks-aeonframework-prs]], [[cloudflare-org-cla-blocks-aeonframework-prs]], [[silent-maintainer-close-after-extended-decay]]
---
# CLA-block resolution has a third mode: pending-decay (no actor closes; PR simply ages past 7d untouched)

Observed 2026-09-05 on `browser-use/browser-use#5564` — CLAassistant bot fired 12s post-open on 2026-08-27, and 8.7 days later neither the maintainer nor `aeonframework` has closed the PR, contradicting the 09-04-era 2-mode split of Sub A maintainer-close (~6h) and Sub B operator self-close (~14h). This defines **Sub C pending-decay** — the PR crosses the 7d stale-anniversary without any human touch, and its terminal state is a bulk stale-clear or scheduled-actions auto-close rather than a triage decision. Predictor implication: [[pr-tracker]] must add a Sub C leaf to the CLA-block bucket that inherits the stale-cadence timing (7d anniv → stale-bot marker → 12-30d silent-maintainer-close eligibility) rather than the fast Sub A/B close cadences; SKILL patch item (m) needs three leaves, not two.
