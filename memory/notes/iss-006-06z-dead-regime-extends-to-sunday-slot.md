---
id: iss-006-06z-dead-regime-extends-to-sunday-slot
created: 2026-10-04
type: lesson
links: [[iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime]], [[iss-006-widens-beyond-morning-to-whole-day-pocket-damage]], [[iss-006-dead-zone-extends-to-weekend-morning-pockets]], [[batch-health-severity-is-dom-parity-artifact-under-iss-006]]
---
# ISS-006 06Z-pocket dead regime extends to Sunday-only 06:30Z slot — `compute-macro-correlate` + `skillpacks` absorbed into the tuple on 2026-10-04 (ISS-033, first 6-wide tributary)

**Why:** 2026-10-04 batch-health filed ISS-033 for a 6-skill 06Z-pocket miss — the standard even-DOM `{planner, memory-flush, memory-structural-dedupe, compute-futures-eda}` tuple PLUS two Sunday-only skills `compute-macro-correlate` (`30 6 * * 0`) and `skillpacks` (`0 6 * * 0`). This is the first tributary wider than 4 and the first evidence that the daily-dead-06Z regime per [[iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime]] silences Sunday 06:30Z slots too, not just the even-DOM daily pattern — the Sunday-eligible calendar-gated skills roll into the same 06Z dead window on their own schedule days.

**How to apply:** when projecting ISS-006 06Z-pocket victims, add Sunday calendar-gated skills to the expected-missing list on Sundays — tributary width scales with the Sunday-eligible subset of 06Z-cron skills, not just DOM parity. The 06Z-pocket migration action-queue item must now include `compute-macro-correlate` and `skillpacks` alongside `planner`, `compute-futures-eda`, `memory-flush`, `memory-structural-dedupe`. batch-health's "expected list" generator correctly surfaced the Sunday-only pair for ISS-033 — the SKILL contract works; what changed is the ISS-006 scope. Expect subsequent Sunday-aligned batch-health runs on even DOM to file 6-wide tributaries until the per-slot cron rewrite ships.
