batch gap — 2026-11-25

2 scheduled skills didn't run in the 06:00–07:30 UTC window:
- planner (30 6 * * *)
- compute-futures-eda (0 6 * * *)

isolated miss — transient cron delay likely. monitoring.
note: 08:00 batch fired at 09:11 UTC today (~1h11 delay), so GHA scheduler was slow this morning.
