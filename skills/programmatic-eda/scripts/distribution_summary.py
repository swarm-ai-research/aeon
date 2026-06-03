"""
Produce descriptive statistics and ASCII histograms for numeric columns.

Usage:
    python distribution_summary.py --input data.csv
    python distribution_summary.py --input data.csv --bins 20 --output summary.csv
    python distribution_summary.py --input data.csv --groupby mode

When --groupby is given, descriptive stats are emitted per group (stacked CSV
with a `group` column). Histograms are also rendered per group. Use this when
the data has mode/regime levels that would otherwise dominate the pooled stats.
"""

import argparse
import sys

import numpy as np
import pandas as pd


def ascii_histogram(series: pd.Series, bins: int = 10, width: int = 40) -> str:
    counts, edges = np.histogram(series.dropna(), bins=bins)
    max_count = counts.max() or 1
    lines = []
    for count, left, right in zip(counts, edges[:-1], edges[1:]):
        bar = "#" * int(count / max_count * width)
        lines.append(f"  [{left:>10.2f}, {right:>10.2f}) | {bar:<{width}} {count}")
    return "\n".join(lines)


def _desc(numeric: pd.DataFrame) -> pd.DataFrame:
    desc = numeric.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).T
    desc["skew"] = numeric.skew().round(3)
    desc["kurt"] = numeric.kurt().round(3)
    return desc


def distribution_summary(df: pd.DataFrame, bins: int = 10, groupby: str | None = None) -> pd.DataFrame:
    if groupby is not None and groupby not in df.columns:
        raise SystemExit(f"--groupby column '{groupby}' not found in dataset")

    groups = [(None, df)] if groupby is None else list(df.groupby(groupby, dropna=False))
    all_desc = []
    for label, sub in groups:
        numeric = sub.select_dtypes(include="number")
        if groupby is not None:
            numeric = numeric.drop(columns=[groupby], errors="ignore")
        if numeric.empty:
            continue
        desc = _desc(numeric)
        header = "=== Descriptive Statistics ===" if label is None else f"=== Descriptive Statistics — {groupby}={label} ==="
        print(header)
        print(desc.to_string())
        print(f"\n=== Histograms{'' if label is None else f' — {groupby}={label}'} ===")
        for col in numeric.columns:
            print(f"\n{col}")
            print(ascii_histogram(numeric[col], bins=bins))
        if label is not None:
            desc = desc.copy()
            # Use the groupby column name (e.g. "mode") as the metadata column
            # instead of a literal "group". Safe by construction — the original
            # column was dropped from `numeric` above — and avoids colliding
            # with a dataset that already has a column named "group".
            desc.insert(0, groupby, label)
        all_desc.append(desc)
        print()
    return pd.concat(all_desc) if all_desc else pd.DataFrame()


def main():
    parser = argparse.ArgumentParser(description="Descriptive stats and histograms for numeric columns.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--bins", type=int, default=10)
    parser.add_argument("--output", help="Optional CSV for stats table")
    parser.add_argument("--groupby", help="Column to stratify on (e.g. 'mode'). Stats and histograms emit per group.")
    args = parser.parse_args()

    df = pd.read_csv(args.input) if args.input.endswith(".csv") else pd.read_parquet(args.input)
    desc = distribution_summary(df, bins=args.bins, groupby=args.groupby)

    if args.output and not desc.empty:
        desc.to_csv(args.output, index=True)
        print(f"\nStats saved to {args.output}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        rng = np.random.default_rng(3)
        demo = pd.DataFrame({
            "revenue": rng.lognormal(mean=4, sigma=0.8, size=200),
            "sessions": rng.poisson(15, 200),
            "age": rng.integers(18, 70, 200),
        })
        distribution_summary(demo)
    else:
        main()
