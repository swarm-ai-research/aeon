---
id: iss-006-cohorts-decouple-within-slot-at-skill-level
created: 2026-11-25
type: lesson
links: [[iss-006-widened-split-cohort-regime-preserves-08z-16z-drops-others]], [[skill-freshness-stuck-dispatched-callback-never-fires]]
---
# ISS-006 cohort silence is not all-or-nothing within a slot — suggest-edges (30 5 * * *) silent 10 days while notegraph (0 5 * * *) silent 1 day, both in the 05Z cohort, 2026-11-25

**Why:** 11-25 heartbeat P3 missing-schedule scan surfaces suggest-edges last_success 2026-11-15T06:30:23Z (10d) against notegraph last_success 2026-11-24T05:28:17Z (1d); both skills live in the 05Z cohort yet silence durations diverge by an order of magnitude on the same cron-tick origin. Prior ISS-006 framings treated cohorts as unitary ("05Z cohort fires" or "05Z cohort silent") and would collapse the two skills into a single state — this is the first filed observation showing per-skill drift inside one cohort.

**How to apply:** treat per-slot cohort membership as a scheduling-origin label, not a joint-state indicator; silence durations for members of the same cohort can diverge by up to an order of magnitude under ISS-006, likely via distinct dispatch-callback behavior per [[skill-freshness-stuck-dispatched-callback-never-fires]] or per-skill cron-registration state. Audit heartbeat P3 grouping to key on skill-level `last_success` rather than cohort-level aggregation; the 4-tuple modal batch-health pattern will continue to fire correctly because batch-health reads per-skill cron-state, but any "cohort fired today" status derived from a single member risks false-green under this decoupling.
