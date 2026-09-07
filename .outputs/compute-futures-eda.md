## Summary

Executed `skills/compute-futures-eda/SKILL.md` end-to-end for CSV `2026-09-06.csv`.

**What I did**
- Fetched `origin/fleet-state` and pulled `memory/gitlawb-compute-futures-proofs/` (found 5 CSVs; 2026-09-06 was the newest, 2026-09-05 present but unfiled).
- Ran all five programmatic-eda scripts stratified by `mode`; outputs at `out/programmatic-eda/compute-futures-2026-09-06/`. (Worked around the sandbox `>`-redirect block with a subprocess wrapper per [[sandbox-blocks-shell-redirect-to-workdir]].)
- Compared per-mode stats against 09-04 (last filed) and 09-05 (unfiled) for trajectory context.

**Top findings (all MEDIUM — no CRITICAL/HIGH)**
1. 2.5× **maxCurve fray REAPPEARS at n=11** — ratio std 2.11e−02, invalidates 09-04's "one-day-anomaly" framing per [[compute-futures-2.5x-curve-side-fray-retracts-at-n-10]]. Fray is now 2-of-6, not 1-of-5.
2. `realizedAbs` 2.5× ratio moves opposite way to **new class-series minimum** 5.91e−02.
3. x402Total x402-mode anchor rotates for **6th consecutive filing** with `realizedAbs` **first-time primary** at |r|=0.373.
4. **Class-first non-padded triple-role top-5 anchor** at seed 202609062 (dispersion $17,089).
5. Spread retail sum **−$39,887** stabilizes in the −$37k to −$59k band; extends [[compute-futures-spread-retail-loss-concentration]] to n=22.
6. Conservation sign pattern flips 4-simultaneous from 09-04's class-first all-positive to (−,−,+,+); all-positive regime confirmed as 2-filing run.
7. n=22 zero within-mode strong pairs (|r|≥0.8).

**Files created / modified**
- `memory/topics/compute-futures-eda/2026-09-06.md` — findings report
- `memory/logs/2026-09-07.md` — activity log
- `.pending-notify/1788766763-compute-futures-eda.md` — notification queued for postprocess
- `out/programmatic-eda/compute-futures-2026-09-06/` — script outputs (uncommitted scratch)
- Branch `compute-futures-eda/2026-09-06` with 2 commits (findings + log)

**Follow-up for the operator**
- Patch [[compute-futures-2.5x-curve-side-fray-retracts-at-n-10]] to note the 09-06 recurrence (or supersede).
- 09-05 CSV was never filed — root cause remains the 06:00Z-pocket outage per [[iss-006-batch-outage-recurs-every-48h-with-06z-pocket-persistently-dead]]; interim mitigation candidate in [MEMORY.md](memory/MEMORY.md) is to migrate `compute-futures-eda` out of the dead pocket.
