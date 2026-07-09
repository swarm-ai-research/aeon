import pandas as pd, os
prior = pd.read_csv("memory/gitlawb-compute-futures-proofs/2026-07-07.csv")
curr = pd.read_csv("memory/gitlawb-compute-futures-proofs/2026-07-08.csv")
print(f"2026-07-07: rows={len(prior)}, cols={len(prior.columns)}, modes={sorted(prior['mode'].unique())}")
print(f"2026-07-08: rows={len(curr)}, cols={len(curr.columns)}, modes={sorted(curr['mode'].unique())}")
print()
print("Column set diff:", set(curr.columns) ^ set(prior.columns))
print()
# Check yesterday's x402Total range
xp = prior[prior["mode"] == "x402"]["x402Total"]
print(f"Prior x402Total: range=${xp[xp>0].min():.2f}-${xp[xp>0].max():.2f}, mean=${xp[xp>0].mean():.2f}, total=${xp.sum():.2f}")
xc = curr[curr["mode"] == "x402"]["x402Total"]
print(f"Curr x402Total: range=${xc[xc>0].min():.2f}-${xc[xc>0].max():.2f}, mean=${xc[xc>0].mean():.2f}, total=${xc.sum():.2f}")
print()
# Check yesterday's spread correlation for realizedAbs x wallet_sum_pnl
for m in ["basket","spread","synthetic","x402"]:
    sub = prior[prior["mode"] == m]
    r_prior = sub[["wallet_sum_pnl","settlementLegs"]].corr().iloc[0,1]
    sub2 = curr[curr["mode"] == m]
    r_curr = sub2[["wallet_sum_pnl","settlementLegs"]].corr().iloc[0,1]
    print(f"{m} wallet_sum_pnl x settlementLegs: prior={r_prior:.3f} curr={r_curr:.3f}")
print()
for m in ["basket","spread","synthetic","x402"]:
    sub = prior[prior["mode"] == m]
    r_prior = sub[["realizedAbs","wallet_sum_pnl"]].corr().iloc[0,1]
    sub2 = curr[curr["mode"] == m]
    r_curr = sub2[["realizedAbs","wallet_sum_pnl"]].corr().iloc[0,1]
    print(f"{m} realizedAbs x wallet_sum_pnl: prior={r_prior:.3f} curr={r_curr:.3f}")
