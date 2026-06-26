batch outage — 2026-06-26 (day 6)

4 skills never triggered (06:00–07:30 UTC):
- planner (30 6 * * *)
- compute-futures-eda (0 6 * * *)
- memory-flush (0 6 2/2 * *) [even-day]
- memory-structural-dedupe (10 6 2/2 * *) [even-day]

even-DOM signature matches days 2 and 4 of ISS-006 exactly. ISS-006 updated with day 6 entry. dead zone still 06:00–06:30 UTC; 05:00 + 05:30 + 08:00 batches all fired. root cause stands (messages.yml `*/5` underdelivery). fix still queued for operator landing.
