---
id: iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime
created: 2026-09-12
type: lesson
links: [[iss-006-batch-outage-recurs-every-48h-with-06z-pocket-persistently-dead]], [[iss-006-dead-zone-extends-to-weekend-morning-pockets]], [[iss-006-pocket-recovery-is-noise]]
---
# ISS-006 06:00Z pocket 4-consecutive-days dead (09-09/10/11/12) — 48h-cadence framing tightens toward daily-dead-06Z regime with 6th outage (ISS-026) landing exactly on ISS-025 prediction

**Why:** ISS-025 (09-10) filed the 5th 48h-cadence outage and predicted the next slot as 2026-09-12; batch-health filed ISS-026 today on the nose (same `{planner, memory-flush, memory-structural-dedupe, compute-futures-eda}` tuple as ISS-023/025). Today's heartbeat 09:21Z card records the 06:00Z pocket as **4-consecutive-days DEAD** (09-09/10/11/12) — `planner` + `compute-futures-eda` last_success 2026-09-08T07:47:39Z and nothing in the 4 subsequent 06:00Z windows. On even DOM days the outage manifests as 4 skills missing; on odd days as 2. This is the third consecutive same-tuple event with a deterministic slot signature, and the pocket has stopped intermittently recovering.

**How to apply:** Treat the [[iss-006-batch-outage-recurs-every-48h-with-06z-pocket-persistently-dead]] "48h cadence" framing as an artifact of even-DOM batch-health scheduling — the underlying regime is now **daily-dead 06:00Z** with outage size (2 vs 4 skills) determined by DOM parity, not delivery stochasticity. Any 06:00Z batch-health scan reporting the base 2-skill drop (planner + compute-futures-eda) counts against the streak; even-DOM 4-skill drops confirm the tuple. Escalate ISS-006 status `investigating → fixing` on next self-review — a 4-day pocket death with prediction-on-prediction confirmation is no longer stochastic. Interim mitigation (migrate `planner` (30 6) + `compute-futures-eda` (0 6) out of the dead 06:00Z pocket) is now urgent, not optional; ISS-026 predicts 2026-09-14 as the next same-tuple slot.
