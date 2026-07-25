#!/usr/bin/env python3
"""Wrapper to run programmatic-eda scripts and capture stdout to files."""
import subprocess
import sys
from pathlib import Path

CSV = "memory/gitlawb-compute-futures-proofs/2026-07-25.csv"
OUT = Path("out/programmatic-eda/compute-futures-2026-07-25")
OUT.mkdir(parents=True, exist_ok=True)

RUNS = [
    ("overview", ["skills/programmatic-eda/scripts/data_overview.py", "--input", CSV, "--sample", "5"]),
    ("nulls", ["skills/programmatic-eda/scripts/null_profiler.py", "--input", CSV, "--output", str(OUT / "nulls.csv")]),
    ("outliers_by_mode", ["skills/programmatic-eda/scripts/outlier_detector.py", "--input", CSV, "--groupby", "mode", "--output", str(OUT / "outliers_by_mode.csv")]),
    ("distributions_by_mode", ["skills/programmatic-eda/scripts/distribution_summary.py", "--input", CSV, "--bins", "8", "--groupby", "mode", "--output", str(OUT / "distributions_by_mode.csv")]),
    ("correlations_by_mode", ["skills/programmatic-eda/scripts/correlation_explorer.py", "--input", CSV, "--groupby", "mode", "--threshold", "0.8", "--output", str(OUT / "correlations_by_mode.csv")]),
]

for name, cmd in RUNS:
    proc = subprocess.run(["python3", *cmd], capture_output=True, text=True)
    (OUT / f"{name}.txt").write_text(proc.stdout + ("\n[stderr]\n" + proc.stderr if proc.stderr else ""))
    print(f"{name}: exit={proc.returncode}, stdout={len(proc.stdout)}B, stderr={len(proc.stderr)}B")
