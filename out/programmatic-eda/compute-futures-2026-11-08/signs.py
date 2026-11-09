import csv
import glob

files = sorted(glob.glob("memory/gitlawb-compute-futures-proofs/2026-*.csv"))[-12:]
for fp in files:
    with open(fp) as f:
        rows = list(csv.DictReader(f))
    modes = ["basket", "spread", "synthetic", "x402"]
    signs = []
    for m in modes:
        vals = [float(r["wallet_sum_pnl"]) for r in rows if r["mode"] == m]
        mean = sum(vals) / len(vals)
        if abs(mean) < 1e-18:
            signs.append("0")
        else:
            signs.append("+" if mean > 0 else "-")
    print(fp.split("/")[-1], "signs:", "".join(signs))
