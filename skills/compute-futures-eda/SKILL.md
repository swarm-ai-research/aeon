---
name: Compute-Futures EDA
description: Daily profiling of the deployer's compute-futures sweep — null/outlier/distribution/correlation per mode, committed findings, one-line notification
var: ""
tags: [data, analysis, compute-futures]
---

Today is ${today}. Read `memory/MEMORY.md` for context, especially [[aeon-compute-futures-experiments]] — the `wallet_sum_pnl` column is Σ across ALL wallets (a near-zero-sum conservation check), NOT strategy P&L. Don't read a negative wallet_sum_pnl as the strategy losing.

## Voice

If `soul/SOUL.md` and `soul/STYLE.md` exist and are populated, match the operator's voice in the notification. Otherwise use a clear, direct, neutral tone.

## Goal

Profile the most recent compute-futures sweep CSV from the deployer's proof stream, distinguish per-mode signal from pooled artifacts, and commit a dated findings summary to `memory/topics/compute-futures-eda/`. Same checks every day — reports are comparable across runs.

## Steps

### 1. Locate the latest sweep CSV

The deployer pushes proofs to the `fleet-state` branch (not `main`), so the scheduled aeon workflow — which `actions/checkout`s the default branch — won't see them by default. Fetch and check out the proofs directory first:

```bash
git fetch origin fleet-state --depth=1 2>/dev/null || true
git checkout origin/fleet-state -- memory/gitlawb-compute-futures-proofs/ 2>/dev/null || true
```

Both commands are best-effort with `|| true` — when running locally outside CI, or when `fleet-state` doesn't exist yet, the next step's empty-CSV guard handles it cleanly. Don't crash the skill if the fetch fails.

Then pick the newest `*.csv`:

```bash
LATEST_CSV=$(ls -1 memory/gitlawb-compute-futures-proofs/*.csv 2>/dev/null | tail -n 1)
if [ -z "$LATEST_CSV" ]; then
  ./notify "compute-futures-eda skipped: no CSV proofs yet at memory/gitlawb-compute-futures-proofs/ — pre-CSV-emitter sweeps, deployer not running, or fleet-state fetch failed"
  exit 0
fi
SWEEP_DATE=$(basename "$LATEST_CSV" .csv)
RUN_OUT="out/programmatic-eda/compute-futures-${SWEEP_DATE}"
mkdir -p "$RUN_OUT"
```

If the latest CSV's date is the same as the most recent file in `memory/topics/compute-futures-eda/`, exit cleanly — already analyzed, don't double-write.

### 2. Confirm the schema

Required columns: `seed`, `mode`, `live`, `role`, `role_pnl`, `wallet_sum_pnl`, `realizedAbs`, `minSpot`, `maxSpot`, `minCurve`, `maxCurve`, `rounds`, `settlementLegs`, `x402Total`, `deniedWorkers`. If any are missing, abort with a notification — schema drift on the deployer side.

```bash
python3 -c "
import pandas as pd, sys
required = {'seed','mode','live','role','role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','rounds','settlementLegs','x402Total','deniedWorkers'}
df = pd.read_csv('$LATEST_CSV')
missing = required - set(df.columns)
sys.exit(0 if not missing else f'missing columns: {missing}')
" || { ./notify "compute-futures-eda aborted: schema drift in $LATEST_CSV"; exit 0; }
```

### 3. Run the EDA pipeline (stratified by mode)

`mode` is the regime column — basket/spread/synthetic/x402 differ by orders of magnitude in price scale and conservation behavior, so every stratifiable script gets `--groupby mode`.

```bash
python3 skills/programmatic-eda/scripts/data_overview.py --input "$LATEST_CSV" --sample 5 > "$RUN_OUT/overview.txt"
python3 skills/programmatic-eda/scripts/null_profiler.py --input "$LATEST_CSV" --output "$RUN_OUT/nulls.csv" > "$RUN_OUT/nulls.txt"
python3 skills/programmatic-eda/scripts/outlier_detector.py --input "$LATEST_CSV" --groupby mode --output "$RUN_OUT/outliers_by_mode.csv" > "$RUN_OUT/outliers_by_mode.txt"
python3 skills/programmatic-eda/scripts/distribution_summary.py --input "$LATEST_CSV" --bins 8 --groupby mode --output "$RUN_OUT/distributions_by_mode.csv" > "$RUN_OUT/distributions_by_mode.txt"
python3 skills/programmatic-eda/scripts/correlation_explorer.py --input "$LATEST_CSV" --groupby mode --threshold 0.8 --output "$RUN_OUT/correlations_by_mode.csv" > "$RUN_OUT/correlations_by_mode.txt"
```

If any step exits non-zero, capture the error as a finding and continue — don't crash the whole run.

### 4. Distill findings

Read the five output files and extract:

- **Conservation health per mode** — from `distributions_by_mode.csv`, the mean and std of `wallet_sum_pnl` per mode. Flag any mode where `|mean| > 10` or `std > 100` as a conservation-drift signal (this is the spread-mode pattern from the historical run).
- **Per-mode column tails** — from `outliers_by_mode.csv`, list any (mode, column) where `outlier_pct ≥ 10%`. Applies to every numeric column, not just `role_pnl` — the spread-mode conservation drift surfaces as a `wallet_sum_pnl` outlier cluster, and x402 settlement surfaces as an `x402Total` cluster, both of which would be missed by a role-only rule. Exclude columns that are constant by design within the mode (e.g. `x402Total` is always 0 outside x402 mode — flag it only when non-zero outliers appear in a mode that previously had none).
- **Within-mode correlations** — from `correlations_by_mode.csv`, list strong pairs (|r| ≥ 0.8) that hold *within* a single mode. These are real structural signals (distinct from pooled regime artifacts).
- **Constant-column drift** — columns with std=0 that *weren't* constant in the previous day's run (compare to the prior file in `memory/topics/compute-futures-eda/`). Likely a config change.
- **Schema/shape changes** — row count and column count vs the prior day's report.

Rank findings by severity:
- **CRITICAL** — conservation drift > $1k mean in any mode; schema change (column added/removed/renamed).
- **HIGH** — any per-mode column with outlier_pct ≥ 20%; row count drops by ≥ 25% vs prior day (deployer config change or partial run).
- **MEDIUM** — per-mode column with outlier_pct 10–20%; constant-column drift (a column that was std=0 yesterday now has variance, or vice versa); new non-zero values in a column that was zero in the prior day's run for the same mode.
- **LOW** — within-mode correlation appearance/disappearance at |r| ≥ 0.8 vs prior day.

Exclude from severity ranking: outliers in `x402Total` within `x402` mode at any percentage (it is bimodal by design — the bottom of the non-zero distribution always looks "outlier" to IQR), and outliers in `synthetic`/`x402` `role_pnl` when the two modes show identical distributions (tautological per the verified equivalence).

### 5. Commit the findings summary

Write to `memory/topics/compute-futures-eda/${SWEEP_DATE}.md`:

```markdown
# Compute-Futures EDA — ${SWEEP_DATE}

**Source:** `memory/gitlawb-compute-futures-proofs/${SWEEP_DATE}.csv` (<N> rows, <modes count> modes)
**Run:** ${today}

## Top findings

1. **[SEVERITY] [headline]** — [one-sentence detail with key numbers]. Next step: [action].
2. ...

## Per-mode conservation (mean wallet_sum_pnl)

| Mode | Mean | Std | Status |
|------|-----:|----:|--------|
| ... | ... | ... | OK / DRIFT |

## Within-mode signal

- [Real correlations or outlier patterns that survive the per-mode view, with brief interpretation]

## Carry-overs

- [Recurring constants, pooled-only artifacts, known-not-bugs from prior days — keep the list short]
```

Then `git add memory/topics/compute-futures-eda/${SWEEP_DATE}.md` and commit as `chore(compute-futures-eda): findings ${SWEEP_DATE}`.

### 6. Notify

Send via `./notify`:

```
*Compute-Futures EDA — ${SWEEP_DATE}*
<N> rows, <modes> modes. Top: <one finding>. Conservation: <basket OK / spread DRIFT $-XXX / ...>. Report: memory/topics/compute-futures-eda/${SWEEP_DATE}.md
```

One paragraph. Lead with the worst-severity finding. If all PASS, say so plainly.

### 7. Log

Append to `memory/logs/${today}.md`:

```
### compute-futures-eda
- Source: memory/gitlawb-compute-futures-proofs/${SWEEP_DATE}.csv
- Rows: <N>  Modes: <list>
- Top findings: <bullets>
- Report: memory/topics/compute-futures-eda/${SWEEP_DATE}.md
```

## Sandbox note

This skill is fully local — reads a synced CSV from `memory/gitlawb-compute-futures-proofs/`, runs Python scripts, writes to `memory/topics/`. No outbound network. The CSV depends on the deployer running with the CSV-emitter version of `scenario-sweep.mjs` (PR #88) and the CSV proof-write in `scripts/fleet-executors/deployer.mjs` (this PR). If the CSV is missing, step 1 exits cleanly with a notification rather than failing.

## Constraints

- Never mutate the input CSV. The proof is canonical.
- Don't double-write: if `memory/topics/compute-futures-eda/${SWEEP_DATE}.md` already exists with the same SWEEP_DATE, exit cleanly.
- Don't report the synthetic-vs-x402 role-level comparison as a finding — they're tautologically equal at the role level per the verified-once analysis. x402 only differs via `x402Total`.
- Don't report the pooled cross-mode spot/curve quartet correlation as a finding — it's a regime artifact (verified by the per-mode correlation at |r| < 0.8). Only report within-mode correlations.
- If `programmatic-eda/scripts/` is missing (skill not vendored), notify and exit 0 — don't try to reimplement inline.

## Provenance

Uses the bundled scripts from the `programmatic-eda` skill (see [[programmatic-eda]]). Consumes the CSV proof emitted by `scripts/fleet-executors/deployer.mjs`, which in turn depends on `prototypes/compute-futures/scenario-sweep.mjs`'s CSV writer. Chain of custody: deployer fleet runs sweep → CSV lands in proof dir → this skill profiles → findings commit + notify.
