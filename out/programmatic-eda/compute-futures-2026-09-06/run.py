#!/usr/bin/env python3
"""Wrapper: run the five programmatic-eda scripts and write stdout to files.

Sandbox blocks `>` redirects to the workdir; subprocess writes bypass that.
Matches [[sandbox-blocks-shell-redirect-to-workdir]].
"""
import subprocess, os, sys

INPUT = "memory/gitlawb-compute-futures-proofs/2026-09-06.csv"
OUT = "out/programmatic-eda/compute-futures-2026-09-06"

def run(cmd, stdout_file):
    p = subprocess.run(cmd, capture_output=True, text=True)
    with open(os.path.join(OUT, stdout_file), "w") as fh:
        fh.write(p.stdout)
    if p.returncode != 0:
        with open(os.path.join(OUT, stdout_file + ".err"), "w") as fh:
            fh.write(p.stderr)
    return p.returncode

rc = 0
rc |= run(["python3", "skills/programmatic-eda/scripts/data_overview.py",
          "--input", INPUT, "--sample", "5"], "overview.txt")
rc |= run(["python3", "skills/programmatic-eda/scripts/null_profiler.py",
          "--input", INPUT, "--output", os.path.join(OUT, "nulls.csv")], "nulls.txt")
rc |= run(["python3", "skills/programmatic-eda/scripts/outlier_detector.py",
          "--input", INPUT, "--groupby", "mode",
          "--output", os.path.join(OUT, "outliers_by_mode.csv")], "outliers_by_mode.txt")
rc |= run(["python3", "skills/programmatic-eda/scripts/distribution_summary.py",
          "--input", INPUT, "--bins", "8", "--groupby", "mode",
          "--output", os.path.join(OUT, "distributions_by_mode.csv")], "distributions_by_mode.txt")
rc |= run(["python3", "skills/programmatic-eda/scripts/correlation_explorer.py",
          "--input", INPUT, "--groupby", "mode", "--threshold", "0.8",
          "--output", os.path.join(OUT, "correlations_by_mode.csv")], "correlations_by_mode.txt")
print("rc", rc)
sys.exit(0)
