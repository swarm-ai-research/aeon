batch outage — 2026-09-06

6 skills never triggered (06:00–07:30 UTC):
- planner (30 6 * * *)
- memory-flush (0 6 2/2 * *, even DOM)
- memory-structural-dedupe (10 6 2/2 * *, even DOM)
- compute-macro-correlate (30 6 * * 0, Sunday)
- compute-futures-eda (0 6 * * *)
- skillpacks (0 6 * * 0, Sunday)

ISS-024 filed. 06:00 pocket now dead 7 consecutive days; 4th ISS-006 outage at 48h cadence. config-validator + swarm-safety-eval fired ~2h late alongside 08:00 pocket. ship interim mitigation — migrate the 06:00 slot skills.
