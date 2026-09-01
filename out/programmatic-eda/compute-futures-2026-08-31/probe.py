import pandas as pd
d = pd.read_csv('out/programmatic-eda/compute-futures-2026-08-31/distributions_by_mode.csv')
print('COLS:', list(d.columns))
for col in ['wallet_sum_pnl', 'role_pnl', 'x402Total', 'settlementLegs', 'realizedAbs', 'maxSpot', 'minCurve', 'minSpot', 'maxCurve']:
    sub = d[d['column'] == col]
    print(f'--- {col} ---')
    print(sub.to_string(index=False))
