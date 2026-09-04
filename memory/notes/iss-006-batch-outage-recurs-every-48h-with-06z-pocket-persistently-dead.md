---
id: iss-006-batch-outage-recurs-every-48h-with-06z-pocket-persistently-dead
created: 2026-09-04
type: lesson
links: [[iss-006-batch-outage-cadence-hypothesis-broken-by-2-day-gap]], [[iss-006-batch-outage-recurs-every-48d-on-same-triple]], [[morning-pocket-splits-into-two-de-facto-clusters]], [[iss-006-pocket-recovery-is-noise]]
---
# ISS-023 filed 2026-09-04 promotes ISS-006 recurrence back to a cadence — 48-HOUR (not 48-day) gaps with `planner` + `compute-futures-eda` dead in the 06:00Z pocket for 5 consecutive days

**Why:** ISS-021 (08-31) → ISS-022 (09-02) → ISS-023 (09-04) hit at exactly 2-day intervals, and `planner` + `compute-futures-eda` have missed the 06:00 pocket for 5 consecutive days (08-31 → 09-04); the even-DOM `memory-flush` + `memory-structural-dedupe` pair adds two more skills on ISS-022/ISS-023. Three data points at 48h supersede the 09-02 "irregular bursts, treat as tomorrow-possible" framing per [[iss-006-batch-outage-cadence-hypothesis-broken-by-2-day-gap]] and the 09-01 "48-day monthly clock" framing per [[iss-006-batch-outage-recurs-every-48d-on-same-triple]]: the 06:00Z pocket is persistently dead, not stochastically dropped, and outage size depends on which other 06:00Z-slot skills are calendar-eligible that day.

**How to apply:** Next predicted outage 2026-09-06 (even DOM, same 4-skill tuple). Any batch-health run on an even day 06:00–07:30Z that reports 4-missing is expected, not novel; on odd days expect the base 2-missing (planner + compute-futures-eda). Escalate ISS-006 status `investigating → fixing` on next self-review — the 48h cadence with a deterministic slot signature is now durable enough to schedule against. Interim mitigation candidate: migrate `planner` (30 6) and `compute-futures-eda` (0 6) out of the dead 06:00 pocket to a known-alive slot until the multi-pocket cron rewrite ships.
