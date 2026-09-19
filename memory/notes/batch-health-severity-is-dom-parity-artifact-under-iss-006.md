---
id: batch-health-severity-is-dom-parity-artifact-under-iss-006
created: 2026-09-19
type: lesson
links: [[iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime]], [[iss-006-dead-pocket-widens-to-08z-heartbeat-miss]], [[iss-006-day-n-needs-witness-independent-of-outage]]
---
# batch-health WARN vs OUTAGE is a DOM-parity artifact under the ISS-006 daily-dead-06Z regime — odd-DOM days lose their ISS filing even when 100% of expected skills miss

**Why:** the 06:00–07:30Z expected list is 4 skills on even DOM (`planner`, `compute-futures-eda`, `memory-flush`, `memory-structural-dedupe` — the latter two run `0 6 2/2 * *` even-only) and 2 skills on odd DOM (`planner`, `compute-futures-eda` only), while SKILL.md line 74 thresholds 1–2 missing → WARN and 3+ → OUTAGE with issue-filing gated to OUTAGE. Under the daily-dead-06Z regime documented in [[iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime]] the pocket takes down 100% of expected members every day, so even-DOM (09-18) hits OUTAGE + ISS-028 filing while odd-DOM (09-19, today) hits WARN + `n/a` filing despite the identical underlying dispatch-silence — the same fault produces different severity classifications by calendar parity alone. Tomorrow's 09-20 Sunday slot is even DOM and will file a 10th ISS-006 tributary; 09-21 Monday odd DOM will drop back to WARN.

**How to apply:** when counting ISS-006 tributaries and severity for post-mortem or fix-priority arguments, decouple the batch-health issue-filing count from the underlying pocket-miss count — every day since 09-08 has been a 06Z pocket miss but only ~half get an ISS number because of DOM parity. Add an odd-DOM WARN witness column to the ISS-006 dead-streak accounting (this note's day 09-19 is the first tracked odd-DOM 100%-miss WARN, joining the ISS-023/025/026/028 even-DOM OUTAGE chain), or lower the OUTAGE threshold to 2+ on days where `expected < 4` so severity encodes fault-rate rather than absolute miss count. Until either lands, do not treat "no ISS filed today" as evidence the pocket has recovered — cross-check `./scripts/skill-runs` for the two daily skills on every calendar day.
