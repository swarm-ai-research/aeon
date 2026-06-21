batch outage — 2026-06-21

6 skills never triggered (06:00–07:30 UTC):
- planner (30 6 * * *)
- compute-futures-eda (0 6 * * *)
- skillpacks (0 6 * * 0)
- compute-macro-correlate (30 6 * * 0)
- config-validator (0 7 * * 0)
- swarm-safety-eval (30 7 * * 0)

ISS-006 filed. GHA cron appears to have dropped the 05:30–08:00 UTC window — 08:00 + 09:00 batches fired together at ~09:05Z. check GHA cron status.
