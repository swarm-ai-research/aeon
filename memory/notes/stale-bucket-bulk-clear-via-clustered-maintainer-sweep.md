---
id: stale-bucket-bulk-clear-via-clustered-maintainer-sweep
created: 2026-08-04
type: observation
links: [[pr-tracker-notify-repeats-with-no-state-change]], [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]], [[maintainer-close-without-merge-triage-pattern]], [[cohort-close-vs-merge-can-split]], [[pr-status]]
---
# Three stale pr-tracker entries broke simultaneously in a 4-minute cross-repo window 2026-08-02T18:29–18:33Z — points to shared upstream advisory-feed signal, not per-repo triage

On 2026-08-02 all three stale-bucket PRs (jamiepine/voicebox#958 tauri, ruvnet/RuView#1409 fastapi, block/buzz#2248 quick-xml) received their first fresh maintainer comments within a 4-minute window (18:29:00Z / 18:33:49Z / 18:29:12Z) across three unrelated repos and maintainer surfaces. Both zero-engagement long-tail stale entries (RuView day 9.8, buzz day 11.7) broke together with voicebox's prior 1-comment stale — same-scan-day cross-repo synchronization is too tight for independent triage, hypothesis is a **shared upstream signal** (security advisory feed refresh or vulnerability aggregator update hitting all three maintainers' notification pipelines simultaneously). Predictor consequence: pr-tracker's tuple-predictor must model bulk-stale-clear as a distinct transition class from per-PR close-follow-through; watch for repeat on 24h / 7d / advisory-publication cadence before promoting from observation to lesson.
