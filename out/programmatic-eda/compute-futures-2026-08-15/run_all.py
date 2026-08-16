"""Run all EDA scripts against the 2026-08-15 CSV and write outputs to files."""
import subprocess
import sys
from pathlib import Path

CSV = "memory/gitlawb-compute-futures-proofs/2026-08-15.csv"
OUT = Path("out/programmatic-eda/compute-futures-2026-08-15")
OUT.mkdir(parents=True, exist_ok=True)

def run(name, args, needs_output=True):
    print(f"--- {name} ---", flush=True)
    cmd = ["python3", f"skills/programmatic-eda/scripts/{name}.py", "--input", CSV] + args
    if needs_output:
        cmd += ["--output", str(OUT / f"{name}.csv")]
    result = subprocess.run(cmd, capture_output=True, text=True)
    (OUT / f"{name}.txt").write_text(result.stdout + ("\n[STDERR]\n" + result.stderr if result.stderr else ""))
    print(f"exit={result.returncode}, wrote {name}.txt", flush=True)
    if result.returncode != 0:
        print("STDERR:", result.stderr[:500], flush=True)

run("data_overview", ["--sample", "5"], needs_output=False)
run("null_profiler", [])
run("outlier_detector", ["--groupby", "mode"])
run("distribution_summary", ["--bins", "8", "--groupby", "mode"])
run("correlation_explorer", ["--groupby", "mode", "--threshold", "0.8"])

print("all done")
