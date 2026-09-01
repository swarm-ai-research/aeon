#!/usr/bin/env bash
set -e
CSV=memory/gitlawb-compute-futures-proofs/2026-08-31.csv
OUT=out/programmatic-eda/compute-futures-2026-08-31
python3 skills/programmatic-eda/scripts/data_overview.py --input "$CSV" --sample 5 > "$OUT/overview.txt"
python3 skills/programmatic-eda/scripts/null_profiler.py --input "$CSV" --output "$OUT/nulls.csv" > "$OUT/nulls.txt"
python3 skills/programmatic-eda/scripts/outlier_detector.py --input "$CSV" --groupby mode --output "$OUT/outliers_by_mode.csv" > "$OUT/outliers_by_mode.txt"
python3 skills/programmatic-eda/scripts/distribution_summary.py --input "$CSV" --bins 8 --groupby mode --output "$OUT/distributions_by_mode.csv" > "$OUT/distributions_by_mode.txt"
python3 skills/programmatic-eda/scripts/correlation_explorer.py --input "$CSV" --groupby mode --threshold 0.8 --output "$OUT/correlations_by_mode.csv" > "$OUT/correlations_by_mode.txt"
echo DONE
