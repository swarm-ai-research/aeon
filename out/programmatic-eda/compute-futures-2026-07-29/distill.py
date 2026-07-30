import pandas as pd
import sys

d = pd.read_csv('out/programmatic-eda/compute-futures-2026-07-29/distributions_by_mode.csv', index_col=0)
d = d.reset_index().rename(columns={'index': 'column'})

def show(col):
    print(f'=== {col} per mode ===')
    print(d[d['column'] == col][['mode', 'count', 'mean', 'std', 'min', 'max']].to_string(index=False))
    print()

for c in ['wallet_sum_pnl', 'role_pnl', 'x402Total', 'settlementLegs', 'realizedAbs', 'maxSpot', 'minSpot', 'minCurve', 'maxCurve']:
    show(c)

print('=== outliers with pct >= 8.0 (excluding seed) ===')
o = pd.read_csv('out/programmatic-eda/compute-futures-2026-07-29/outliers_by_mode.csv')
o = o[(o['outlier_pct'] >= 8.0) & (o['column'] != 'seed')]
print(o[['mode', 'column', 'outlier_count', 'outlier_pct', 'min', 'max', 'mean']].to_string(index=False))
print()

print('=== raw CSV summary ===')
raw = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-07-29.csv')
print(f'rows={len(raw)}, cols={len(raw.columns)}, seeds={sorted(raw["seed"].unique())}')
print()
print('mode counts:')
print(raw['mode'].value_counts().to_string())
print()

# constants by design
print('=== constants ===')
print('rounds:', raw['rounds'].unique())
print('deniedWorkers:', raw['deniedWorkers'].unique())
print('live per mode:')
print(raw.groupby('mode')['live'].unique().to_string())
print('settlement per mode:')
print(raw.groupby('mode')['settlement'].unique().to_string())
print('spotSource per mode:')
print(raw.groupby('mode')['spotSource'].unique().to_string())

# check spread wallet_sum_pnl abs range
print()
print('=== wallet_sum_pnl abs by mode ===')
for m in raw['mode'].unique():
    v = raw[raw['mode'] == m]['wallet_sum_pnl']
    print(f'{m}: absmax={v.abs().max():.3e}, range={v.max()-v.min():.3e}, std={v.std():.3e}')

# settlementLegs per mode distribution
print()
print('=== settlementLegs distribution per mode ===')
for m in raw['mode'].unique():
    v = raw[raw['mode'] == m]['settlementLegs']
    print(f'{m}: {v.value_counts().sort_index().to_dict()}')

# x402Total in x402
print()
print('=== x402Total in x402 ===')
xv = raw[raw['mode'] == 'x402']['x402Total']
print(f'sum={xv.sum():.2f}, mean={xv.mean():.2f}, min={xv.min():.2f}, max={xv.max():.2f}')

# check maxSpot per seed in each mode - anchor detection
print()
print('=== max maxSpot per mode + associated seed ===')
for m in raw['mode'].unique():
    sub = raw[raw['mode'] == m]
    top = sub.nlargest(3, 'maxSpot')[['seed', 'maxSpot']].drop_duplicates()
    print(f'{m}: top-3 seeds by maxSpot:')
    print(top.to_string(index=False))
    print()
