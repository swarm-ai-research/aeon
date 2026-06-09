import pandas as pd
pd.set_option('display.float_format', lambda x: f'{x:.4g}')
d = pd.read_csv('out/programmatic-eda/compute-futures-2026-06-08/distributions_by_mode.csv').rename(columns={'Unnamed: 0':'column'})
print('=== wallet_sum_pnl by mode ===')
print(d[d['column']=='wallet_sum_pnl'][['mode','count','mean','std','min','max']].to_string(index=False))
print('\n=== role_pnl by mode ===')
print(d[d['column']=='role_pnl'][['mode','count','mean','std','min','max']].to_string(index=False))
print('\n=== x402Total by mode ===')
print(d[d['column']=='x402Total'][['mode','count','mean','std','min','max']].to_string(index=False))
print('\n=== realizedAbs by mode ===')
print(d[d['column']=='realizedAbs'][['mode','count','mean','std','min','max']].to_string(index=False))
print('\n=== minSpot/maxSpot/minCurve/maxCurve by mode ===')
sub = d[d['column'].isin(['minSpot','maxSpot','minCurve','maxCurve'])][['column','mode','mean','min','max']]
print(sub.to_string(index=False))
print('\n=== rounds/settlementLegs/deniedWorkers by mode ===')
sub = d[d['column'].isin(['rounds','settlementLegs','deniedWorkers'])][['column','mode','mean','std','min','max']]
print(sub.to_string(index=False))

print('\n\n=== OUTLIERS by mode (only >=10% pct) ===')
o = pd.read_csv('out/programmatic-eda/compute-futures-2026-06-08/outliers_by_mode.csv')
o.columns = [c.lower() for c in o.columns]
print('outlier columns:', list(o.columns))
print(o.head(3))
PYEOF_END
