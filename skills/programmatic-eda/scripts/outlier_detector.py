"""
Detect outliers in numeric columns using IQR and z-score methods.

Usage:
    python outlier_detector.py --input data.csv
    python outlier_detector.py --input data.csv --method iqr --output outliers.csv
    python outlier_detector.py --input data.csv --groupby mode --output outliers.csv

When --groupby is given, IQR/z-score thresholds are computed within each group
(e.g. per `mode`) and the output has one row per (group × column). This avoids
flooding the report with "outliers" that are actually structural level
differences between groups (e.g. frontier-model rows at 100× commodity prices).
"""

import argparse
import sys

import numpy as np
import pandas as pd


def detect_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    return (series < q1 - k * iqr) | (series > q3 + k * iqr)


def detect_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    z = (series - series.mean()) / series.std(ddof=1)
    return z.abs() > threshold


def _summarize(df: pd.DataFrame, method: str, k: float, z_thresh: float, group_label=None, group_col: str = "group") -> list:
    numeric = df.select_dtypes(include="number").columns
    rows = []
    for col in numeric:
        s = df[col].dropna()
        if len(s) < 4:
            continue
        iqr_mask = detect_iqr(s, k) if method in ("iqr", "both") else pd.Series(False, index=s.index)
        z_mask = detect_zscore(s, z_thresh) if method in ("zscore", "both") else pd.Series(False, index=s.index)
        combined = iqr_mask | z_mask
        row = {
            "column": col,
            "outlier_count": int(combined.sum()),
            "outlier_pct": round(combined.mean() * 100, 2),
            "min": s.min(),
            "max": s.max(),
            "mean": round(s.mean(), 4),
            "iqr_outliers": int(iqr_mask.sum()),
            "zscore_outliers": int(z_mask.sum()),
        }
        if group_label is not None:
            row = {group_col: group_label, **row}
        rows.append(row)
    return rows


_EMPTY_COLS = ["column", "outlier_count", "outlier_pct", "min", "max", "mean", "iqr_outliers", "zscore_outliers"]


def detect_outliers(df: pd.DataFrame, method: str = "both", k: float = 1.5, z_thresh: float = 3.0, groupby: str | None = None) -> pd.DataFrame:
    if groupby is None:
        rows = _summarize(df, method, k, z_thresh)
        if not rows:
            return pd.DataFrame(columns=_EMPTY_COLS)
        return pd.DataFrame(rows).sort_values("outlier_count", ascending=False)
    if groupby not in df.columns:
        raise SystemExit(f"--groupby column '{groupby}' not found in dataset")
    # Use the user's groupby column name as the metadata column. The original
    # `groupby` column is dropped from the data passed to _summarize, so the
    # name is free to reuse — and using it (instead of a literal "group") makes
    # the output schema readable AND sidesteps collisions when the dataset
    # already has a column literally named "group".
    rows = []
    for value, sub in df.groupby(groupby, dropna=False):
        rows.extend(_summarize(sub.drop(columns=[groupby]), method, k, z_thresh, group_label=value, group_col=groupby))
    if not rows:
        return pd.DataFrame(columns=[groupby, *_EMPTY_COLS])
    return pd.DataFrame(rows).sort_values([groupby, "outlier_count"], ascending=[True, False])


def main():
    parser = argparse.ArgumentParser(description="Detect outliers via IQR and/or z-score.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--method", choices=["iqr", "zscore", "both"], default="both")
    parser.add_argument("--iqr-k", type=float, default=1.5, help="IQR multiplier (default 1.5)")
    parser.add_argument("--z-thresh", type=float, default=3.0, help="Z-score threshold (default 3)")
    parser.add_argument("--output", help="Optional CSV output path")
    parser.add_argument("--groupby", help="Column to stratify on (e.g. 'mode'). Outlier detection runs within each group.")
    args = parser.parse_args()

    df = pd.read_csv(args.input) if args.input.endswith(".csv") else pd.read_parquet(args.input)
    result = detect_outliers(df, method=args.method, k=args.iqr_k, z_thresh=args.z_thresh, groupby=args.groupby)
    print(result.to_string(index=False))
    if args.output:
        result.to_csv(args.output, index=False)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        rng = np.random.default_rng(2)
        demo = pd.DataFrame({
            "revenue": np.concatenate([rng.normal(100, 10, 95), [500, 600, 700, -200, 1000]]),
            "sessions": rng.poisson(20, 100),
            "age": np.concatenate([rng.integers(18, 65, 98), [120, 150]]),
        })
        print(detect_outliers(demo).to_string(index=False))
    else:
        main()
