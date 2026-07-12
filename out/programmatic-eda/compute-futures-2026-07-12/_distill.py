import pandas as pd
pd.set_option('display.width', 220)

dist = pd.read_csv("out/programmatic-eda/compute-futures-2026-07-12/distributions_by_mode.csv")
dist = dist.rename(columns={'Unnamed: 0': 'column'})

for col in ['wallet_sum_pnl','role_pnl','x402Total','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs','rounds','deniedWorkers']:
    print(f"== {col} per mode ==")
    print(dist[dist['column']==col][['column','mode','mean','std','min','max']].to_string(index=False))
    print()

# Row counts per mode
print("== row counts per mode ==")
print(dist[dist['column']=='role_pnl'][['mode','count']].to_string(index=False))
