import pandas as pd
import numpy as np

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-10-22.csv')
# Pivot per (seed, role) to compare basket vs synthetic
# Spot columns are per-seed deterministic; take first row per (seed, mode) using role analyst
basket = df[df['mode'] == 'basket'].groupby('seed').first().reset_index()
synth = df[df['mode'] == 'synthetic'].groupby('seed').first().reset_index()

merged = basket[['seed', 'minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'realizedAbs']].merge(
    synth[['seed', 'minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'realizedAbs']],
    on='seed', suffixes=('_basket', '_synth'))

for col in ['minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'realizedAbs']:
    merged[f'ratio_{col}'] = merged[f'{col}_basket'] / merged[f'{col}_synth']

print('Per-seed ratios:')
print(merged[['seed'] + [f'ratio_{c}' for c in ['minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'realizedAbs']]].to_string(index=False))

print()
print('Ratio summary (mean / std / unique):')
for col in ['minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'realizedAbs']:
    r = merged[f'ratio_{col}']
    print(f'  {col}: mean={r.mean():.6f}  std={r.std():.6e}  unique={r.nunique()}  min={r.min():.6f}  max={r.max():.6f}')

print()
print('Unique seeds (padded?):', sorted(df['seed'].unique().tolist()))

# Compare role-level synth vs x402 for 8 shared cols
synth_full = df[df['mode'] == 'synthetic'].sort_values(['seed', 'role']).reset_index(drop=True)
x402_full = df[df['mode'] == 'x402'].sort_values(['seed', 'role']).reset_index(drop=True)
shared_cols = ['role_pnl', 'wallet_sum_pnl', 'realizedAbs', 'minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'settlementLegs']
print()
print('max abs diff synth vs x402 per shared column:')
for c in shared_cols:
    d = (synth_full[c] - x402_full[c]).abs().max()
    print(f'  {c}: {d}')

# Spread retail top-loss analysis
print()
print('--- spread retail top-6 losses ---')
sp = df[df['mode'] == 'spread'].sort_values('role_pnl').head(6)
print(sp[['seed', 'role', 'role_pnl']].to_string(index=False))

# Role means in spread
print()
print('--- spread role means ---')
print(df[df['mode'] == 'spread'].groupby('role')['role_pnl'].agg(['mean', 'count']).to_string())

# Non-padded vs padded split in spread retail
spread_retail = df[(df['mode'] == 'spread') & (df['role'] == 'retail')].copy()
spread_retail['padded'] = spread_retail['seed'] > 1e9
print()
print('--- spread retail padded vs non-padded ---')
print(spread_retail.groupby('padded')['role_pnl'].agg(['count', 'mean']).to_string())

# x402Total summary
print()
x402_df = df[df['mode'] == 'x402']
print(f'x402Total: mean={x402_df["x402Total"].mean():.2f}  std={x402_df["x402Total"].std():.2f}  min={x402_df["x402Total"].min():.2f}  max={x402_df["x402Total"].max():.2f}  range={x402_df["x402Total"].max() - x402_df["x402Total"].min():.2f}')

# Spot-column coupling
print()
print('--- within-mode minSpot x maxSpot correlation (non-padded) ---')
for m in ['basket', 'spread', 'synthetic', 'x402']:
    sub = df[(df['mode'] == m) & (df['seed'] <= 1e9)]
    r = sub['minSpot'].corr(sub['maxSpot'])
    print(f'  {m}: r={r:.4f}  n={len(sub)}')
