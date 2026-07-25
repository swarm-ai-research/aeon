import pandas as pd

d = pd.read_csv('out/programmatic-eda/compute-futures-2026-07-25/distributions_by_mode.csv')
d = d.rename(columns={'Unnamed: 0':'column'})
cols = ['wallet_sum_pnl','role_pnl','realizedAbs','x402Total','maxSpot','minSpot','settlementLegs','minCurve','maxCurve']
for c in cols:
    sub = d[d['column']==c][['mode','count','mean','std','min','max','25%','50%','75%']]
    print(f'\n=== {c} by mode ===')
    print(sub.to_string(index=False))

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-07-25.csv')
print('\n=== spread wallet_sum_pnl absolute magnitude ===')
w = df[df['mode']=='spread']['wallet_sum_pnl']
print('absmax:', w.abs().max(), 'sum:', w.sum(), 'std:', w.std())
print('\n=== basket wallet_sum_pnl absolute magnitude ===')
w = df[df['mode']=='basket']['wallet_sum_pnl']
print('absmax:', w.abs().max(), 'sum:', w.sum(), 'std:', w.std())
print('\n=== synthetic wallet_sum_pnl absolute magnitude ===')
w = df[df['mode']=='synthetic']['wallet_sum_pnl']
print('absmax:', w.abs().max(), 'sum:', w.sum(), 'std:', w.std())
print('\n=== x402 wallet_sum_pnl absolute magnitude ===')
w = df[df['mode']=='x402']['wallet_sum_pnl']
print('absmax:', w.abs().max(), 'sum:', w.sum(), 'std:', w.std())

# Check synthetic vs x402 equivalence
print('\n=== synth vs x402 role_pnl diff ===')
s = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
x = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)
for c in ['role_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs']:
    print(f'{c} max_abs_diff:', (s[c]-x[c]).abs().max())

# x402Total total
print('\n=== x402Total in x402 mode ===')
x402 = df[df['mode']=='x402']['x402Total']
print('sum:', x402.sum(), 'mean:', x402.mean(), 'min:', x402.min(), 'max:', x402.max(), 'std:', x402.std())

# Basket realizedAbs deeper inspection
print('\n=== basket realizedAbs distribution ===')
b = df[df['mode']=='basket'][['seed','role','realizedAbs']].sort_values('realizedAbs')
print(b.to_string(index=False))

# Basket settlementLegs — 16.67% outliers today
print('\n=== basket settlementLegs distribution ===')
b = df[df['mode']=='basket']['settlementLegs'].value_counts().sort_index()
print(b.to_string())

# Spread maxSpot — 25% outliers, new HIGH
print('\n=== spread maxSpot distribution ===')
s = df[df['mode']=='spread'][['seed','role','maxSpot']].sort_values('maxSpot')
print(s.to_string(index=False))

# Basket role_pnl σ
print('\n=== basket role_pnl σ ===')
print(df[df['mode']=='basket']['role_pnl'].agg(['mean','std','min','max']).to_string())

# Spread role_pnl σ
print('\n=== spread role_pnl σ ===')
print(df[df['mode']=='spread']['role_pnl'].agg(['mean','std','min','max']).to_string())

# Synth role_pnl σ
print('\n=== synth role_pnl σ ===')
print(df[df['mode']=='synthetic']['role_pnl'].agg(['mean','std','min','max']).to_string())

# Seed encoding
print('\n=== seed string lengths ===')
seed_lens = df['seed'].astype(str).str.len().value_counts().sort_index()
print(seed_lens.to_string())
