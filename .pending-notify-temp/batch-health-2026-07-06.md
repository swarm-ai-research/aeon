batch outage — 2026-07-06 (day 16 of ISS-006)

5 skills never triggered in the 06:00–07:30 UTC window:
- planner (30 6 * * *)
- compute-futures-eda (0 6 * * *)
- memory-flush (0 6 2/2 * *) — even DOM
- memory-structural-dedupe (10 6 2/2 * *) — even DOM
- cost-report (0 7 * * 1) — weekly Mon slot

selective survival: notegraph/suggest-edges fired on time at 05:37Z; 08:00 + 09:00 batches flushed together at 09:43Z (1h43m / 43m late). 06:00–07:30 pocket outside messages.yml catch-up window.

yesterday's 07:44Z flush burst was noise, not resolution — today's clean relapse confirms per [[iss-006-pocket-recovery-is-noise]]. ISS-006 day-16 update appended (not filing new issue — duplicate root cause). fix still queued: replace messages.yml `*/5` with explicit per-slot crons.
