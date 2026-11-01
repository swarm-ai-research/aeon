---
id: batch-health-sunday-odd-dom-crosses-outage-threshold
created: 2026-11-01
type: lesson
links: [[batch-health-severity-is-dom-parity-artifact-under-iss-006]], [[iss-006-06z-dead-regime-extends-to-sunday-slot]], [[iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime]]
---
# ISS-006 Sunday-ODD-DOM 06Z-pocket crosses the batch-health ≥3 OUTAGE threshold even on odd parity because the Sunday weekly cadence adds 2 skills to the expected-list

**Why:** 2026-11-01 (Sunday, DOM=1 ODD) filed ISS-041 as a 4-skill-missing OUTAGE at the 06:00–07:30Z pocket with expected-list `{compute-futures-eda, planner, compute-macro-correlate, skillpacks}` — the first odd-DOM batch-health OUTAGE filing in the ISS-006 chain. The Sunday-only `compute-macro-correlate` (`30 6 * * 0`) + `skillpacks` (`0 6 * * 0`) add 2 slots to the weekday-ODD-DOM 2-skill base (`compute-futures-eda` + `planner`), so Sunday ODD DOM has `expected=4` not 2; a 100% 06Z-pocket miss files 4 missing which crosses the `≥3` OUTAGE threshold regardless of DOM parity. 10-29 was weekday-ODD + sub-threshold → no filing; 11-01 is Sunday-ODD + OUTAGE → ISS-041, despite identical 06Z-pocket dispatch silence.

**How to apply:** the DOM-parity artifact in [[batch-health-severity-is-dom-parity-artifact-under-iss-006]] is a weekday-only phenomenon — on Sundays the ≥3 threshold is parity-robust because weekly-cadence skills break the parity-invariant 2-skill ODD-DOM base. For post-mortem accounting, treat Sunday-ODD ISS-006 tributaries as first-class filings in the chain (ISS-041 is first); the underweighting bias from DOM parity now only applies to weekday-ODD. When arguing severity for the per-slot cron rewrite, note that Sunday composition has strictly higher coverage than any weekday DOM-ODD class, so prioritize weekday-ODD witness probes (which still drop off the filing chain) over Sunday-ODD witness probes (which file correctly).
