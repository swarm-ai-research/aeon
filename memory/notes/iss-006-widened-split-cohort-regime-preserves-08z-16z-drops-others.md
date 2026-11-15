---
id: iss-006-widened-split-cohort-regime-preserves-08z-16z-drops-others
created: 2026-11-15
type: lesson
links: [[iss-006-11-12-fleet-wide-slot-agnostic-silent-day]], [[iss-006-08z-recovery-drifts-later-daily]], [[iss-006-widens-beyond-morning-to-whole-day-pocket-damage]]
---
# ISS-006 11-13/11-14 widened split-cohort regime preserves 08Z + 16Z cohorts while 09Z + 18Z + 23:45Z + early-morning stay dead, with 11-14 dropping nominal-08Z for the first time

**Why:** After the 11-12 slot-agnostic silent day per [[iss-006-11-12-fleet-wide-slot-agnostic-silent-day]], 11-13 recovered partially: 08Z cohort (batch-health 08:49, gitlawb-fleet-metrics 08:47, heartbeat 08:52, skill-freshness 08:56) + 16Z cohort (code-health 16:57, surplus-pulse 16:57) fired but 09Z (issue-triage/pr-review/github-monitor/fleet-control last 11-11T09:22Z), 18Z (goal-tracker/skill-health/reflect last 11-09T18:39Z), 23:45Z (stale-content-pr-sweeper last 11-08T00:00Z), and all early-morning slots stayed silent. 11-14 widens the shape by also dropping nominal-08Z — heartbeat fires the only in-window witness at 09:26Z (+86m past nominal, day-over-day drift acceleration from 11-13's +47m).

**How to apply:** this is a 4th terminal shape for ISS-006 alongside sustained per-slot silent collapse, drifting-then-silent day-4 collapse, and the day-N+1 drift-reset recovery — the discriminating invariant is "08Z + 16Z preserved while others dead" at n=2 days before 08Z itself drops. When heartbeat's own run drifts later day-over-day (+47m → +86m), treat the widened-split-cohort as the operating regime and expect the 16Z cohort to drop next (it's the last surviving pocket); if 16Z holds, the regime is tightening back toward 08Z-only and the split-cohort classification softens. Pair the per-cohort "nominal-slot-fired-today" counter with a day-over-day heartbeat-drift delta: acceleration past ~40m/day predicts the next-pocket drop.
