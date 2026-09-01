#!/usr/bin/env python3
import subprocess, sys, pathlib

CSV = "memory/gitlawb-compute-futures-proofs/2026-08-31.csv"
OUT = pathlib.Path("out/programmatic-eda/compute-futures-2026-08-31")
OUT.mkdir(parents=True, exist_ok=True)

steps = [
    ("overview", ["python3", "skills/programmatic-eda/scripts/data_overview.py", "--input", CSV, "--sample", "5"], None),
    ("nulls", ["python3", "skills/programmatic-eda/scripts/null_profiler.py", "--input", CSV, "--output", str(OUT / "nulls.csv")], None),
    ("outliers_by_mode", ["python3", "skills/programmatic-eda/scripts/outlier_detector.py", "--input", CSV, "--groupby", "mode", "--output", str(OUT / "outliers_by_mode.csv")], None),
    ("distributions_by_mode", ["python3", "skills/programmatic-eda/scripts/distribution_summary.py", "--input", CSV, "--bins", "8", "--groupby", "mode", "--output", str(OUT / "distributions_by_mode.csv")], None),
    ("correlations_by_mode", ["python3", "skills/programmatic-eda/scripts/correlation_explorer.py", "--input", CSV, "--groupby", "mode", "--threshold", "0.8", "--output", str(OUT / "correlations_by_mode.csv")], None),
]

for name, cmd, _ in steps:
    print(f"== {name} ==", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    (OUT / f"{name}.txt").write_text(r.stdout)
    if r.returncode != 0:
        (OUT / f"{name}.err").write_text(r.stderr)
        print(f"FAIL {name}: rc={r.returncode}", flush=True)
    else:
        print(f"OK {name}", flush=True)
print("DONE")
