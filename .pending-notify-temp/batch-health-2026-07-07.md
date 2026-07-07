batch gap — 2026-07-07

2 scheduled skills didn't run in the 06:00–07:30 UTC window:
- planner (`30 6 * * *`)
- compute-futures-eda (`0 6 * * *`)

WARN by count, but this is Day 17 of ISS-006 (messages.yml `*/5` underdelivery). Same odd-DOM signature as days 3/5. batch-health itself fired ~54min late (08:54Z). Fix still queued — replace `*/5` with explicit per-slot crons.
