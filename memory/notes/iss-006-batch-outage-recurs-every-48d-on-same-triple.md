---
id: iss-006-batch-outage-recurs-every-48d-on-same-triple
created: 2026-09-01
type: lesson
links: [[iss-006-day-n-needs-witness-independent-of-outage]], [[iss-006-pocket-recovery-is-noise]], [[morning-pocket-splits-into-two-de-facto-clusters]], [[planner-silenced-by-its-own-escalation-target]]
---
# ISS-006's morning-pocket outage has replayed the exact same missing triple `[planner, compute-futures-eda, cost-report]` on 2026-07-14 (ISS-019) / 2026-08-03 (ISS-020) / 2026-08-31 (ISS-021), a 48-day recurrence window with byte-identical signature

Three morning batch-outage tributary issues in 48 days, all filed by `batch-health` against the same 06:00–07:30Z expected-list and all missing the same three skills — planner (`30 6 * * *`), compute-futures-eda (`0 6 * * *`), and cost-report (`0 7 * * 1`) — with matching same-day 08:00 batch late-fire tails at ~2h lag. The recurrence cadence is close enough to monthly (~48d) that the underlying `messages.yml` `*/5` underdelivery is now durable-pattern territory, not stochastic delivery-rate noise — the fix path (per-slot crons for every `aeon.yml` timeslot) is the same one queued since day 5, but the recurrence signature warrants promoting ISS-006 status `investigating → fixing` on next self-review. Downstream predictor: the next replay lands around 2026-10-18 ± a few days if the pattern is monthly; a fourth same-triple outage before that date is a delivery-cadence acceleration signal worth escalating further.
