"""Scan multiplier trajectory across the gap-day CSVs 11-08 -> 11-14."""
import csv
from collections import defaultdict

DATES = ["2026-11-08", "2026-11-10", "2026-11-11", "2026-11-12", "2026-11-13", "2026-11-14"]

for d in DATES:
    path = f"memory/gitlawb-compute-futures-proofs/{d}.csv"
    try:
        with open(path) as f:
            rows = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"{d}: missing")
        continue
    basket = [r for r in rows if r["mode"] == "basket"]
    synth = [r for r in rows if r["mode"] == "synthetic"]
    spread = [r for r in rows if r["mode"] == "spread"]
    x402 = [r for r in rows if r["mode"] == "x402"]
    if len(basket) == len(synth) and len(basket) > 0:
        ratios = [float(basket[i]["maxSpot"]) / float(synth[i]["maxSpot"]) for i in range(len(basket)) if float(synth[i]["maxSpot"]) != 0]
        uniq_ratios = sorted(set(round(r, 6) for r in ratios))
        mean_r = sum(ratios) / len(ratios)
    else:
        mean_r = None
        uniq_ratios = []

    # Conservation sign pattern
    def sign(mode_rows):
        if not mode_rows:
            return "?"
        vals = [float(r["wallet_sum_pnl"]) for r in mode_rows]
        m = sum(vals) / len(vals)
        return "+" if m > 0 else "-" if m < 0 else "0"
    sign_pat = sign(basket) + sign(spread) + sign(synth) + sign(x402)

    # Spread retail top-6
    spread_sorted = sorted(spread, key=lambda r: float(r["role_pnl"]))
    retail_count = sum(1 for r in spread_sorted[:6] if r["role"] == "retail")

    # x402Total
    xvals = [float(r["x402Total"]) for r in x402 if float(r["x402Total"]) != 0]
    if xvals:
        xmean = sum(xvals) / len(xvals)
        xmin = min(xvals)
        xmax = max(xvals)
    else:
        xmean = xmin = xmax = 0

    print(f"{d}: mult(maxSpot)={mean_r:.8f} uniq_vals={uniq_ratios} signs={sign_pat} spread_top6_retail={retail_count}/6 x402Total(mean/min/max)=${xmean:.2f}/${xmin:.2f}/${xmax:.2f}")
