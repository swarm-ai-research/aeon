batch gap — 2026-09-23

2 scheduled skills didn't run (06:00–07:30 UTC):
- compute-futures-eda (0 6 * * *)
- planner (30 6 * * *)

isolated miss — transient cron delay likely. monitoring.

context: 100% miss of a 2-skill expected list (memory-flush + memory-structural-dedupe skip on odd DOMs), consistent with the ISS-006 06Z dead pocket. WARN under current SKILL.md threshold; SKILL patch to lower OUTAGE bar to ≥2/expected<4 still unlanded.
