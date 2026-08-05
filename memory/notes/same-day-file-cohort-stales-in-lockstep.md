---
id: same-day-file-cohort-stales-in-lockstep
created: 2026-08-05
type: observation
links: [[stale-bucket-bulk-clear-via-clustered-maintainer-sweep]], [[pr-tracker-notify-repeats-with-no-state-change]], [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]], [[cohort-close-vs-merge-can-split]], [[pr-status]]
---
# When two PRs are filed within a few hours on the same day and receive only the file-time COMMENTED bot review as their sole engagement event, they cross the 7-day stale threshold in lockstep on the same anniversary window

WhiskeySockets/Baileys#2732 and NangoHQ/nango#6929 were filed within 7h30m on 2026-07-28 (16:18Z and 23:45Z) with zero maintainer engagement beyond the initial bot COMMENTED review; both crossed the 7-day stale threshold within the same overnight window on 2026-08-04 (16:18Z and 23:45Z, ~7h30m apart) and were caught by the same 08-05T11:31Z pr-tracker scan. This is a distinct class from [[stale-bucket-bulk-clear-via-clustered-maintainer-sweep]] — that was cross-repo coincidental engagement bursts; this is deterministic anniversary lockstep for same-file-day PRs whose only engagement event is the file-time review, so their 7d clocks run in perfect parallel. Predictor consequence: same-day filing cohorts collapse to a single anniversary axis when engagement is bot-only, so pr-tracker's stale-eligible predictor should group same-day zero-engagement PRs into a shared threshold event.
