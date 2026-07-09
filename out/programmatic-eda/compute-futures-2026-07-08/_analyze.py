import pandas as pd
d = pd.read_csv("out/programmatic-eda/compute-futures-2026-07-08/distributions_by_mode.csv")
d = d.rename(columns={"Unnamed: 0": "column"})
for col in ["wallet_sum_pnl","role_pnl","realizedAbs","x402Total","settlementLegs","minSpot","maxSpot"]:
    print(f"\n=== {col} per mode ===")
    print(d[d["column"] == col][["column","mode","count","mean","std","min","max"]].to_string(index=False))
