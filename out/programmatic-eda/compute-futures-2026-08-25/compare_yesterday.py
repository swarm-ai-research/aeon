import pandas as pd
df24 = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-08-24.csv')
df25 = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-08-25.csv')

print('=== 08-24 x402 correlations of interest ===')
x24 = df24[df24['mode']=='x402']
for c in ['minSpot','maxSpot','minCurve','maxCurve','settlementLegs','realizedAbs','wallet_sum_pnl']:
    print(f'  {c} x x402Total: {x24[c].corr(x24["x402Total"]):.4f}')

print()
print('=== 08-25 x402 correlations of interest ===')
x25 = df25[df25['mode']=='x402']
for c in ['minSpot','maxSpot','minCurve','maxCurve','settlementLegs','realizedAbs','wallet_sum_pnl']:
    print(f'  {c} x x402Total: {x25[c].corr(x25["x402Total"]):.4f}')

print()
print('=== 08-24 x402Total stats ===')
print(f'  min={x24["x402Total"].min():.4f} max={x24["x402Total"].max():.4f} range={x24["x402Total"].max()-x24["x402Total"].min():.4f} mean={x24["x402Total"].mean():.4f} std={x24["x402Total"].std():.4f}')

print()
print('=== 08-25 x402Total stats ===')
print(f'  min={x25["x402Total"].min():.4f} max={x25["x402Total"].max():.4f} range={x25["x402Total"].max()-x25["x402Total"].min():.4f} mean={x25["x402Total"].mean():.4f} std={x25["x402Total"].std():.4f}')

print()
print('=== 08-24 settlementLegs distribution per mode ===')
print(df24.groupby('mode')['settlementLegs'].agg(['min','max','mean','std','nunique']))
print(df24.groupby('mode')['settlementLegs'].apply(lambda s: s.value_counts().head(3).to_dict()))

print()
print('=== 08-25 settlementLegs distribution per mode ===')
print(df25.groupby('mode')['settlementLegs'].agg(['min','max','mean','std','nunique']))
print(df25.groupby('mode')['settlementLegs'].apply(lambda s: s.value_counts().head(3).to_dict()))
