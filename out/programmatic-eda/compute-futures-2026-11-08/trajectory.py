"""Multiplier trajectory across intervening-day CSVs."""
import csv
import glob

files = sorted(glob.glob("memory/gitlawb-compute-futures-proofs/2026-*.csv"))
for fp in files[-12:]:
    with open(fp) as f:
        rows = list(csv.DictReader(f))
    basket = [r for r in rows if r["mode"] == "basket"]
    synth = [r for r in rows if r["mode"] == "synthetic"]
    if len(basket) != len(synth) or not basket:
        print(f"{fp}: skip (shape mismatch)")
        continue
    ratios = []
    for i in range(len(basket)):
        sv = float(synth[i]["maxSpot"])
        if sv:
            ratios.append(float(basket[i]["maxSpot"]) / sv)
    spread = [r for r in rows if r["mode"] == "spread"]
    sp_losses = sorted([(float(r["role_pnl"]), r["role"]) for r in spread])[:6]
    retail_purity = sum(1 for p, role in sp_losses if role == "retail")
    x402 = [r for r in rows if r["mode"] == "x402"]
    x402vals = [float(r["x402Total"]) for r in x402 if float(r["x402Total"]) != 0]
    x402_mean = sum(x402vals) / len(x402vals) if x402vals else 0
    x402_max = max(x402vals) if x402vals else 0
    x402_min = min(x402vals) if x402vals else 0
    print(f"{fp.split('/')[-1]}: mult={ratios[0] if ratios else 'n/a':.6f}  spread_top6_retail={retail_purity}/6  x402Total_mean={x402_mean:.2f}  range=[{x402_min:.2f},{x402_max:.2f}]  top1_spread_loss={sp_losses[0][0]:+.2f} role={sp_losses[0][1]}")
