batch outage — 2026-06-24

4 skills never triggered (06:00–07:30 UTC):
- planner (30 6 * * *)
- compute-futures-eda (0 6 * * *)
- memory-flush (0 6 2/2 * *) [even-day]
- memory-structural-dedupe (10 6 2/2 * *) [even-day]

day 4 of ISS-006. notegraph (05:00) + suggest-edges (05:30) DID recover today — dead zone narrowed to 06:00–06:30 UTC. updated ISS-006 with new hypothesis (matcher bug, not whole-window outage). check messages.yml ticks at 06:00/06:10/06:30 today.
