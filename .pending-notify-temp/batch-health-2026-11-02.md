batch outage — 2026-11-02

5 skills never triggered (06:00–07:30 UTC):
- compute-futures-eda (0 6 * * *)
- memory-flush (0 6 2/2 * *)
- memory-structural-dedupe (10 6 2/2 * *)
- planner (30 6 * * *)
- cost-report (0 7 * * 1)

ISS-042 filed. check GHA cron status — Monday-even 5-tuple, cost-report absorbed into ISS-006 chain for the first time.
