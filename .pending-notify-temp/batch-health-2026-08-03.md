batch outage — 2026-08-03

3 skills never triggered (06:00–07:30 UTC):
- planner (30 6 * * *)
- compute-futures-eda (0 6 * * *)
- cost-report (0 7 * * 1)

08:00Z pocket also stuck — cluster of 10 skills all fired at 09:57:58–09:58:31Z (~118min late, +5min vs 08-02's 113min). Pocket migration confirmed per 08-02 escalation gate. ISS-020 filed; ISS-006 close-clock reset. Check GHA cron status.
