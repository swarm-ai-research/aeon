---
name: Programmatic EDA
description: Systematic exploratory data analysis on a dataset — structure, nulls, outliers, distributions, correlations — and produce a shareable profiling report
var: ""
tags: [data, analysis]
---
> **${var}** — Path to the dataset to profile (CSV or Parquet — Excel is auto-converted to CSV). Relative to repo root. **Required.** Example: `data/orders_2026q2.csv`.

<!-- Wrapped from nimrodfisher/data-analytics-skills — programmatic-eda. Upstream scripts/references/assets preserved verbatim under this skill's folder. -->

Read `memory/MEMORY.md` for context.

If `${var}` is empty, notify and exit:
```bash
./notify "programmatic-eda skipped: var empty — pass dataset path e.g. var=data/foo.csv"
exit 0
```

If the file at `${var}` does not exist, notify and exit:
```bash
[ -f "${var}" ] || { ./notify "programmatic-eda aborted: dataset not found at ${var}"; exit 0; }
```

## Goal

Run a fixed profiling pipeline on `${var}`, classify findings, and ship a Markdown report + a short findings summary. Same checks every run so reports are comparable across datasets.

## Steps

### 1. Prepare environment

Ensure Python deps are available. The bundled scripts use only `pandas` and `numpy` (no scipy / matplotlib — histograms are ASCII, descriptive stats are pandas-native). If `${var}` is a Parquet file, `pyarrow` is also required — `pd.read_parquet` will fail without an engine even though pandas itself imports fine. If an import fails, run `pip install --quiet pandas numpy pyarrow` and retry once.

Inputs supported by the scripts: `.csv` and `.parquet`. If `${var}` ends in `.xlsx` / `.xls`, convert to CSV first (`python -c "import pandas as pd; pd.read_excel('${var}').to_csv('/tmp/eda-input.csv', index=False)"`) and use the converted path for the rest of the run.

All bundled scripts use `--input <path>` (CSV or Parquet). Set `RUN_OUT=out/programmatic-eda/$(basename ${var} | sed 's/\.[^.]*$//')-${today}` and `mkdir -p "$RUN_OUT"` before step 2.

### 2. Load and overview

Run `python skills/programmatic-eda/scripts/data_overview.py --input ${var} --sample 10 | tee "$RUN_OUT/overview.txt"`. Capture row count, dtypes, memory, sample. Confirm the **grain** (what one row represents) — if ambiguous, note it as an open question in the findings summary rather than guessing.

### 3. Null profile

Read warn/fail thresholds from `skills/programmatic-eda/references/quality_thresholds.md` (defaults: warn 5%, fail 30%). Run `python skills/programmatic-eda/scripts/null_profiler.py --input ${var} --warn-pct <W> --fail-pct <F> --output "$RUN_OUT/nulls.csv" | tee "$RUN_OUT/nulls.txt"`. Flag every column marked `FAIL` (and any `WARN` that crosses a column-specific override in the thresholds doc).

### 4. Outlier detection

Run `python skills/programmatic-eda/scripts/outlier_detector.py --input ${var} --method both --output "$RUN_OUT/outliers.csv" | tee "$RUN_OUT/outliers.txt"` (IQR + z-score on numerics). For each flagged column, classify the spike: *real signal* (keep) vs *data error* (recommend fix). Don't drop anything — this skill profiles, it doesn't mutate.

If the dataset has a categorical regime column (e.g. `mode`, `cohort`, `segment`) whose levels differ by ≥10× in scale, pooled outlier detection misleads — higher-regime rows get flagged as outliers when they're just routine for their level. Re-run with `--groupby <col>` to stratify thresholds within each level, and treat the grouped output as the authoritative one.

### 5. Distribution summary

Run `python skills/programmatic-eda/scripts/distribution_summary.py --input ${var} --bins 20 --output "$RUN_OUT/distributions.csv" | tee "$RUN_OUT/distributions.txt"`. The script emits descriptive stats and ASCII histograms — both land in the tee'd file.

If a `--groupby` was warranted in step 4, pass the same column here (`--groupby <col>`) so stats and histograms emit per group — pooled descriptives over a multi-regime column hide the structure.

### 6. Correlation exploration

Run `python skills/programmatic-eda/scripts/correlation_explorer.py --input ${var} --threshold 0.8 --output "$RUN_OUT/correlations.csv" | tee "$RUN_OUT/correlations.txt"`. Flag pairs with |r| ≥ 0.8 as potential multicollinearity or redundancy. Note any surprising zero-correlations between columns that *should* be related.

If a `--groupby` was warranted in step 4, pass the same column here (`--groupby <col>`) — pooled correlation can be dominated by between-group level differences, so a strong pooled `r` may vanish or flip sign within each regime. The stacked per-group output lets you tell structural collinearity (consistent within every group) from regime-driven artifacts (only present pooled or in one group).

### 7. Checklist sign-off

Walk `skills/programmatic-eda/references/eda_checklist.md`. Confirm each item before declaring profiling complete; any unchecked item becomes a line in the findings summary.

### 8. Write deliverables

- Fill `skills/programmatic-eda/assets/eda_report_template.md` into the run output directory as `eda_report.md` — full per-column profiling output.
- Fill `skills/programmatic-eda/assets/findings_summary.md` into the run output directory as `findings_summary.md` — top 3–5 issues with severity (CRITICAL / HIGH / MEDIUM / LOW) and a recommended next step for each.

### 9. Notify

Send via `./notify`:
```
*Programmatic EDA — $(basename ${var})*
Rows: <N>  Cols: <M>  Grain: <one row = ...>
Top issues: <issue 1> · <issue 2> · <issue 3>
Report: out/programmatic-eda/<run-dir>/eda_report.md
```

Keep it one paragraph (per Aeon notification rules).

### 10. Log

Append to `memory/logs/${today}.md`:
```
### programmatic-eda
- Dataset: ${var}
- Rows / Cols: <N> / <M>
- Top findings: <bullet list>
- Output: out/programmatic-eda/<run-dir>/
```

## Sandbox note

This skill is fully local — it reads a file from the repo and runs Python scripts. No outbound network is required, so the WebFetch fallback pattern doesn't apply. If a script needs a package the runner doesn't have, install via `pip install --quiet` (pandas/numpy/scipy/matplotlib are the only deps the bundled scripts use).

If `${var}` points at a remote URL instead of a local path: fetch it once via `curl -L -o /tmp/eda-input.<ext> ${var}` (with WebFetch fallback), then run the pipeline against the local copy.

## Constraints

- Never mutate the input dataset. This skill profiles; it does not clean.
- Bundled scripts have no skip-list arg, so PII filtering happens at the reporting layer: when summarizing distribution/correlation output, exclude columns whose name matches obvious PII patterns (email, ssn, phone, address) — these are noise for EDA and a leak risk in the report.
- Don't crash on a single failing step — log it as a finding ("step X failed: <reason>"), continue with the remaining steps, and surface the failure in the notification.
- Don't downgrade thresholds to make a dataset look clean. If `quality_thresholds.md` flags something, it flags something.

## Provenance

Scripts, references, and asset templates are vendored from [nimrodfisher/data-analytics-skills](https://github.com/nimrodfisher/data-analytics-skills) (`01-data-quality-validation/programmatic-eda/`). Upstream license applies. To pull upstream updates, re-copy the three subfolders; SKILL.md is Aeon-specific and should not be overwritten.
