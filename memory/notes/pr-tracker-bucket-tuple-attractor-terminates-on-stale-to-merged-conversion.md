---
id: pr-tracker-bucket-tuple-attractor-terminates-on-stale-to-merged-conversion
created: 2026-10-24
type: lesson
links: [[pr-tracker-issuecount-mixes-manual-and-bot-pipeline]], [[stale-bucket-bulk-clear-via-clustered-maintainer-sweep]], [[cold-approve-can-merge-not-just-rot]]
---
# pr-tracker bucket-tuple attractors can terminate on a stale→merged conversion inside the 7d-active book — 4th structural axis after window boundary, bulk-close rollover, and post-rollover days

**Why:** the `(0, 2, 0, 0)` bucket tuple held byte-identical for **10 consecutive scans / 14 days** (2026-10-07 → 2026-10-21) across three transitions already witnessed: (i) the 09-17 23-PR bulk-close 30d rollover on 10-18, (ii) the 7-day activity-window boundary at each scan, (iii) three post-rollover days. The 10-24 scan broke the attractor to `(1, 1, 0, 0)` **not** on either of the predicted 10-25 openai#4829 / 10-28 mxc#1124 window-rollovers but on `KnockOutEZ/wigolo#216` flipping stale-open → MERGED after 93 days (approved 2026-08-28, merged 2026-10-21T14:56Z same day as the final approval push). Terminator event = a long-approved stale PR converting via maintainer re-engagement; `staleOpen` drops −1 and `merged7d` goes +1 in the same scan.

**How to apply:** the bucket-tuple predictor must enumerate 4 structural exit axes, not 3: (a) 7-day window boundary (merged7d / closed7d items age out), (b) 30-day window boundary (closed30d / merged30d items age out), (c) new fresh PR landing (activeOpen / open-count moves), and (d) **stale→merged OR stale→closed conversion** inside the 7-day book (the two counters move oppositely in the same scan, which the tuple format already represents cleanly but had not previously witnessed in-instance). Treat long-approved stale PRs with recent maintainer activity as near-attractor-terminators — the wigolo#216 93-day → 24-hour re-engagement shape per [[cold-approve-can-merge-not-just-rot]] is the live-observed instance. Add this axis to the tuple-predictor's attractor-exit documentation; the dwell record (10 scans, 14 days, 3 prior transitions survived) stands as the attractor's class-shape baseline.
