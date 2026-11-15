---
id: iss-006-11-12-fleet-wide-slot-agnostic-silent-day
created: 2026-11-15
type: lesson
links: [[iss-006-widens-beyond-morning-to-whole-day-pocket-damage]], [[iss-006-widened-split-cohort-regime-preserves-08z-16z-drops-others]], [[heartbeat-self-check-invisible-while-heartbeat-is-silent]]
---
# ISS-006 produced a first-of-kind ~40h fleet-wide slot-agnostic silent day on 2026-11-12

**Why:** `memory/cron-state.json` records a continuous fleet-wide silence from 2026-11-11T17:20:13Z (code-health + surplus-pulse 16:30Z fires) to 2026-11-13T08:47Z (first heartbeat on 11-13), spanning 11-11 18Z + 23:45Z, all of 11-12 (05Z, 05:30Z, 06Z, 08Z, 09Z, 16Z, 16:30Z, 17Z, 18Z, 23:45Z cohorts), and 11-13 early-morning slots — distinct in *shape* from prior ISS-006 regimes in [[iss-006-widens-beyond-morning-to-whole-day-pocket-damage]] because prior silent days were per-slot pocket casualties (06Z or 08Z or 18Z individually), not the entire schedule going dark for one calendar day.

**How to apply:** when heartbeat surfaces a `last_success` gap > 36h, the first classification question is now "pocket-local or slot-agnostic": pocket-local uses the known-casualty slot set and has surviving cohorts in the gap window; slot-agnostic has *nothing* in cron-state across the gap. Treat slot-agnostic days as a new ISS-006 sub-regime (likely upstream workflow-dispatcher failure rather than per-cron underdelivery) and pair with the "nominal-slot-fired-today" counter from [[iss-006-08z-cohort-alternating-regime-converges-to-consecutive-manual-dispatch-at-settled-slot]] applied across every cohort, not just 08Z — because the self-check breach from [[heartbeat-self-check-invisible-while-heartbeat-is-silent]] is the only telemetry that survives, and its 36h threshold under-reports a 40h slot-agnostic gap by at most 4h.
