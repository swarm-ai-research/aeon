batch gap — 2026-06-23 (day 3 recurring)

2 scheduled skills didn't run in 06:00–07:30 UTC:
- planner (30 6 * * * daily)
- compute-futures-eda (0 6 * * * daily)

same two daily skills missed 06:00–06:30 slot 2026-06-21, 06-22 (batch-health coverage gap), and today. not transient — recurring signature.

ISS-006 bumped medium→high, status investigating. likely workflow auto-disable or schedule-field drift on those two workflows specifically. other 08:00 batch (heartbeat, skill-freshness, gitlawb-fleet-metrics) fired normally.

next: inspect Actions tab for planner.yml + compute-futures-eda.yml enablement; `gh workflow enable` if disabled.
