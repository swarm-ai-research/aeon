## Summary

Executed `compute-futures-eda` skill for 2026-07-17.

**Pipeline:** Fetched `origin/fleet-state`, checked out `memory/gitlawb-compute-futures-proofs/` (5 CSVs 07-13 → 07-17), confirmed schema (144 rows × 17 cols, 4 modes), ran the 5 programmatic-eda scripts stratified by mode (pandas + numpy installed locally at session start).

**Top findings:**
- **[HIGH]** `minSpot` outlier_pct hits 25% simultaneously in basket, synthetic, and x402 — 9/36 rows per mode tag IQR whiskers (first three-mode co-fire in the record, but consistent with 12-seed IQR-tight-band artifact).
- **[MEDIUM]** Wide new outlier surface across `maxSpot` (all 4 modes at 16.67%) and `maxCurve` (basket new + synth/x402 holds). 9 new (mode, column) MEDIUM+ flags plus one carry-over vs 07-16.
- **[MEDIUM]** synth/x402 `maxCurve` at 16.67% — first (mode, column) pair to persist across two runs since the record starts.
- **[LOW]** Fourth consecutive filed run with zero |r|≥0.8 correlations. x402 `settlementLegs × x402Total` fourth sign-flip in five runs.
- **[PASS]** Conservation healthy in every mode (max |mean| 1.09e−12, spread; 12+ orders under thresholds). Schema intact. Synth ≡ x402 tautology reconfirmed (max |diff role_pnl| = 0.0).

**Files:**
- `memory/topics/compute-futures-eda/2026-07-17.md` (new, committed as `chore(compute-futures-eda): findings 2026-07-17`, pushed).
- `memory/logs/2026-07-18.md` (appended, committed as `chore(logs): compute-futures-eda entry 2026-07-17`, pushed).
- `.pending-notify/1784355954-compute-futures-eda.md` (direct write per [[notify-inline-cat-substitution-blocked-in-sandbox]]).

**Follow-up:** Next CSV determines whether today's wider outlier surface is a real signal shift or 12-seed jitter. Same-column persistence on `minSpot` in three modes → escalates to signal; rotation → continues 12-seed instability classification per [[compute-futures-12-seed-sample-too-small]].
