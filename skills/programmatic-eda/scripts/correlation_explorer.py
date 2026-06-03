"""
Compute pairwise correlations for numeric columns and flag strong pairs.

Usage:
    python correlation_explorer.py --input data.csv
    python correlation_explorer.py --input data.csv --threshold 0.7 --output corr.csv
    python correlation_explorer.py --input data.csv --groupby mode

When --groupby is given, a correlation matrix and strong-pair list are emitted
per group. The output CSV stacks matrices with a `group` column so downstream
tools can split. Use this when pooled correlations are dominated by between-
group level differences and you want to see what's true within each regime.
"""

import argparse
import sys

import numpy as np
import pandas as pd


def find_strong_pairs(corr_matrix: pd.DataFrame, threshold: float = 0.8) -> pd.DataFrame:
    pairs = []
    cols = corr_matrix.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            val = corr_matrix.iloc[i, j]
            if pd.notna(val) and abs(val) >= threshold:
                pairs.append({"col_a": cols[i], "col_b": cols[j], "correlation": round(val, 4)})
    if not pairs:
        return pd.DataFrame(columns=["col_a", "col_b", "correlation"])
    return pd.DataFrame(pairs).sort_values("correlation", key=abs, ascending=False)


def _explore_one(numeric: pd.DataFrame, threshold: float, method: str, label=None) -> pd.DataFrame:
    if numeric.shape[1] < 2 or len(numeric) < 3:
        suffix = "" if label is None else f" — {label}"
        print(f"Skipped{suffix}: need ≥2 numeric columns and ≥3 rows.")
        return pd.DataFrame()
    corr = numeric.corr(method=method)
    header_suffix = "" if label is None else f" — {label}"
    print(f"=== Correlation Matrix ({method}){header_suffix} ===")
    print(corr.round(3).to_string())
    pairs = find_strong_pairs(corr, threshold=threshold)
    print(f"\n=== Strong Pairs (|r| ≥ {threshold}){header_suffix} ===")
    if pairs.empty:
        print("  None found.")
    else:
        print(pairs.to_string(index=False))
    print()
    return corr


def explore_correlations(df: pd.DataFrame, threshold: float = 0.8, method: str = "pearson", groupby: str | None = None) -> pd.DataFrame:
    if groupby is not None and groupby not in df.columns:
        raise SystemExit(f"--groupby column '{groupby}' not found in dataset")
    if groupby is None:
        return _explore_one(df.select_dtypes(include="number"), threshold, method)
    matrices = []
    for value, sub in df.groupby(groupby, dropna=False):
        numeric = sub.select_dtypes(include="number").drop(columns=[groupby], errors="ignore")
        corr = _explore_one(numeric, threshold, method, label=f"{groupby}={value}")
        if not corr.empty:
            corr = corr.copy()
            # Use the groupby column name (e.g. "mode") as the metadata column.
            # Safe by construction — the original column was dropped via
            # `.drop(columns=[groupby], ...)` above — and prevents colliding
            # with a dataset that already has a column named "group".
            corr.insert(0, groupby, value)
            matrices.append(corr)
    return pd.concat(matrices) if matrices else pd.DataFrame()


def main():
    parser = argparse.ArgumentParser(description="Explore pairwise correlations and flag strong pairs.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--threshold", type=float, default=0.8, help="Abs correlation threshold (default 0.8)")
    parser.add_argument("--method", choices=["pearson", "spearman", "kendall"], default="pearson")
    parser.add_argument("--output", help="Optional CSV output for correlation matrix")
    parser.add_argument("--groupby", help="Column to stratify on (e.g. 'mode'). Correlation matrix emits per group.")
    args = parser.parse_args()

    df = pd.read_csv(args.input) if args.input.endswith(".csv") else pd.read_parquet(args.input)
    matrix = explore_correlations(df, threshold=args.threshold, method=args.method, groupby=args.groupby)

    if args.output and not matrix.empty:
        matrix.to_csv(args.output)
        print(f"Matrix saved to {args.output}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        rng = np.random.default_rng(4)
        base = rng.normal(0, 1, 200)
        demo = pd.DataFrame({
            "revenue": base * 100 + rng.normal(0, 5, 200),
            "gross_profit": base * 80 + rng.normal(0, 8, 200),  # high corr with revenue
            "sessions": rng.poisson(20, 200),
            "bounce_rate": rng.uniform(0.2, 0.9, 200),
        })
        explore_correlations(demo, threshold=0.7)
    else:
        main()
