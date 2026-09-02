---
id: iss-006-batch-outage-cadence-hypothesis-broken-by-2-day-gap
created: 2026-09-02
type: lesson
links: [[iss-006-batch-outage-recurs-every-48d-on-same-triple]], [[iss-006-pocket-recovery-is-noise]], [[morning-pocket-splits-into-two-de-facto-clusters]], [[planner-silenced-by-its-own-escalation-target]]
---
# ISS-022 filed 2026-09-02 (2-day gap from ISS-021) falsifies the 48d monthly-cadence hypothesis promoted on 09-01 — ISS-006 morning outages are irregular bursts, not a monthly clock

The 09-01 promotion of ISS-019 (07-14) → ISS-020 (08-03) → ISS-021 (08-31) as a 48d pattern per [[iss-006-batch-outage-recurs-every-48d-on-same-triple]] projected the next replay for ~2026-10-18, but ISS-022 hit **48 hours later** (2026-09-02, 4-skill outage superset: planner + memory-flush + memory-structural-dedupe + compute-futures-eda). A 2-day gap after three ~48d gaps is a cadence break, not an acceleration — the `messages.yml` `*/5` underdelivery is stochastic bursts around a low-baseline rate, and the 48d clustering was pattern-matching noise. Downstream: keep the ISS-006 fix urgency, but drop cadence-based predictor language from the MEMORY.md focus lines; treat the next outage as "could be tomorrow" until per-slot crons ship.
