Skill executed successfully. Summary below.

## Summary

**Skill:** `compute-futures-eda` — daily profiling of the deployer's compute-futures sweep for 2026-07-25.

**What ran:**
1. Fetched `origin/fleet-state` proofs → located `memory/gitlawb-compute-futures-proofs/2026-07-25.csv` (144 rows, 4 modes, all 17 columns present, zero nulls).
2. Confirmed the report file for 2026-07-25 didn't yet exist (last filing 2026-07-24, 1-day gap).
3. Ran all 5 `programmatic-eda` scripts (overview / nulls / outliers / distributions / correlations) stratified by `mode`. All exit=0.
4. Cross-referenced against 07-24 filings and the historical rotation-pattern series (07-09 → 07-24) for outlier_pct trajectories and the x402 sign-flip streak.
5. Wrote `memory/topics/compute-futures-eda/2026-07-25.md` (13 numbered findings + per-mode conservation table + within-mode signal section + shape diff + carry-overs).
6. Committed as `chore(compute-futures-eda): findings 2026-07-25` (commit `29d9595`, findings file only — fleet-state proofs left untracked as they belong on that branch).
7. Queued notification at `.pending-notify/1784961981-compute-futures-eda.md`.
8. Appended entry to `memory/logs/2026-07-25.md`.

**Headline findings:**
- **HIGH** — Spread `maxSpot` outlier_pct **25.00%**, first appearance in the record at ≥ 20% for this (mode, column). Anchored by seed 202607255 at $74.95 (≈$5 gap above the next-highest seed).
- **MEDIUM ×2 (collapses)** — Both of 07-24's escalation-gate flags failed at first re-check: basket `realizedAbs` 25.00% → 0.00% (HIGH gate fails), and spread `minSpot` 16.67% → 0.00% (three-run persistence-candidate class breaks; class remains empty).
- **MEDIUM (rotation continues)** — Basket `settlementLegs` 16.67% re-fires after 07-24 collapse (5th 16.67% fire in last 10 filings).
- **LOW** — Fresh basket near-miss `realizedAbs × settlementLegs` = +0.776; x402 `settlementLegs × x402Total` = +0.357 (third consecutive positive, sign-flip streak stays broken).
- **PASS** — Conservation healthy every mode, schema/shape intact vs 07-24, ninth consecutive run at zero |r| ≥ 0.8.

**Files created/modified:**
- `memory/topics/compute-futures-eda/2026-07-25.md` (committed, 61 lines)
- `memory/logs/2026-07-25.md` (appended, unstaged — matches daily-log pattern)
- `.pending-notify/1784961981-compute-futures-eda.md` (queued for post-run delivery)
- `out/programmatic-eda/compute-futures-2026-07-25/` (5 EDA outputs + wrapper scripts; scratch)

**Follow-up:**
- Watch spread `maxSpot` on 2026-07-26 — if it holds ≥ 10%, promote to persistence-candidate; if it collapses (as basket `realizedAbs` did today), reclassify as jitter.
- The 07-24 promotion criteria (three-run same-magnitude streak) is now empirically shown too permissive at 12 seeds. Consider tightening — the only structural fix remains seed-count widening per [[compute-futures-12-seed-sample-too-small]].
