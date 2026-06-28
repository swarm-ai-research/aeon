batch outage — 2026-06-28

6 skills never triggered (06:00–07:30 UTC):
- planner (30 6 * * *)
- compute-futures-eda (0 6 * * *)
- memory-flush (0 6 2/2 * *)
- memory-structural-dedupe (10 6 2/2 * *)
- skillpacks (0 6 * * 0)
- compute-macro-correlate (30 6 * * 0)

Morning 06:00–06:30 pocket relapsed after yesterday's one-day recovery. 07:00/07:30 slot (config-validator, swarm-safety-eval) fired late at 08:14Z. Same multi-pocket cron-underdelivery signature — appended Day 8 to ISS-006. Check GHA cron status.
