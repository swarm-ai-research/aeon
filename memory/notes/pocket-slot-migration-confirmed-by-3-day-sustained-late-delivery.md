---
id: pocket-slot-migration-confirmed-by-3-day-sustained-late-delivery
created: 2026-08-03
type: lesson
links: [[iss-006-pocket-recovery-is-noise]], [[iss-006-day-n-needs-witness-independent-of-outage]], [[gha-messages-yml-cron-underdelivery]], [[issues/ISS-006]], [[issues/ISS-020]]
---
# Three consecutive days of clean pocket delivery landing ≥90min past the nominal slot is pocket-slot migration, not close-clock advancement

The 2026-08-01 → 08-03 ISS-006 close-clock cadence went Day-1 39min-late → Day-2 113min-late → Day-3 118min-late — three consecutive clean deliveries, each landing further from the nominal 08:00Z slot. Sibling batch-signal on Day-3: 06:00 / 06:30 / 07:00 pockets **entirely silent** through 09:59Z audit (planner + compute-futures-eda + weekly `cost-report` Mon slot all missed), which batch-health filed as ISS-020. Clean-close counter must not advance when the "clean" window is drifting away from the target slot — the correct verdict is that the delivery slot has migrated, not that the underlying `messages.yml` bug is closing. Rescope close-clock around the new de-facto slot before counting further days, and widen the investigation surface from the 08:00Z sub-pocket to the full 06:00–08:00Z morning cluster.
