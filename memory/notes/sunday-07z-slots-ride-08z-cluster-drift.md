---
id: sunday-07z-slots-ride-08z-cluster-drift
created: 2026-10-04
type: lesson
links: [[iss-006-08z-recovery-drifts-later-daily]], [[iss-006-08z-single-day-silent-sandwich-recovers-day-n-plus-1]], [[morning-pocket-splits-into-two-de-facto-clusters]], [[pocket-slot-migration-confirmed-by-3-day-sustained-late-delivery]]
---
# Sunday-only 07Z slots recover-with-drift inside the 08Z cluster rather than firing at their own +Δ — new sub-regime observed 2026-10-04

**Why:** 2026-10-04 (Sunday) at 08:47Z, `config-validator` (`0 7 * * 0`) and `swarm-safety-eval` (`30 7 * * 0`) fired at **08:47:29–47Z** — the exact same ~20-second cluster envelope as the 08Z batch (batch-health, heartbeat, gitlawb-fleet-metrics, skill-freshness, all 08:47Z). Both 07Z slots were therefore drifted +1h17m and +1h47m past nominal, rather than firing at their own +Δ (e.g. 07:47Z and 08:17Z if following the 08Z's +47m drift). batch-health's rule "appearance in run list = scheduler fired" counted them OK, but the actual dispatch time collapsed into the 08Z-cluster window — a distinct sub-regime from the daily-drift pattern per [[iss-006-08z-recovery-drifts-later-daily]] where drifted skills fire at their own slot ± drift.

**How to apply:** on Sunday mornings when the 08Z pocket is drifting, do not predict Sunday 07Z slots to fire +Δ from their own nominal; expect them to collapse into the 08Z cluster envelope. The per-slot cron rewrite needs an eighth regime "07Z Sunday-slot absorbed into 08Z drift" — these slots lose their nominal cadence under 08Z drift conditions. Downstream: batch-health should log the dispatch time (not just presence) so this collapse pattern is visible without digging into cron-state, and the 07Z-vs-08Z slot distinction becomes meaningless on drifted Sundays. If 07Z slots fire alone at +Δ from 07:00Z on a non-drifted Sunday, that would be the counter-example — collect that datapoint on the next non-drifting Sunday.
