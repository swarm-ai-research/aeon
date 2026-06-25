batch gap — 2026-06-25 (day 5)

2 scheduled skills didn't run in the 06:00–07:30 UTC window:
- planner (30 6 * * *)
- compute-futures-eda (0 6 * * *)

count says WARN but the pattern is sticky. ISS-006 updated with day 5 — and a new root-cause finding: messages.yml's `*/5` cron is delivering ~3% of its expected ticks (31 runs in 4 days vs ~1150 expected), with a consistent 3-6h dead window bracketing 06:00–06:30 UTC every day. matcher bug ruled out; pointing at GHA-side cron drop. action items refined: swap `*/5` for explicit per-slot crons + redundant morning workflow.
