"""Extract per-mode + cross-day metrics for 08-15 findings."""
import pandas as pd
import numpy as np

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-08-15.csv')

print('=== spread role_pnl by role ===')
spread = df[df['mode']=='spread']
print(spread.groupby('role')['role_pnl'].agg(['count','mean','std','min','max']).round(2))
print()

# basket/synth ratios (per-seed, ignoring role since prices are same across roles)
print('=== basket/synth ratios (deterministic scale check) ===')
basket = df[df['mode']=='basket'].groupby('seed').agg({'minSpot':'first','maxSpot':'first','minCurve':'first','maxCurve':'first','realizedAbs':'first'})
synth = df[df['mode']=='synthetic'].groupby('seed').agg({'minSpot':'first','maxSpot':'first','minCurve':'first','maxCurve':'first','realizedAbs':'first'})
common = basket.index.intersection(synth.index)
ratios = (basket.loc[common] / synth.loc[common])
print(ratios.agg(['min','max','mean','std']).round(6))
print()

# x402Total range
print('=== x402 x402Total distribution ===')
x402 = df[df['mode']=='x402']
print(f'min={x402["x402Total"].min():.2f}, max={x402["x402Total"].max():.2f}, mean={x402["x402Total"].mean():.2f}, std={x402["x402Total"].std():.2f}, sum={x402["x402Total"].sum():.2f}')
# who anchors LOW and HIGH?
low_x = x402[x402['x402Total']==x402['x402Total'].min()][['seed','role','x402Total']]
high_x = x402[x402['x402Total']==x402['x402Total'].max()][['seed','role','x402Total']]
print('LOW anchor:', low_x.to_dict('records'))
print('HIGH anchor:', high_x.to_dict('records'))
print()

# wallet_sum_pnl per mode
print('=== wallet_sum_pnl conservation per mode ===')
for m in ['basket','spread','synthetic','x402']:
    ws = df[df['mode']==m]['wallet_sum_pnl']
    print(f'{m}: mean={ws.mean():.3e}, std={ws.std():.3e}, min={ws.min():.3e}, max={ws.max():.3e}')
print()

# x402 settlementLegs × x402Total correlation
xcorr = x402[['settlementLegs','x402Total']].corr().iloc[0,1]
print(f'x402 settlementLegs × x402Total corr = {xcorr:.4f}')
print()

# Anchor concentration - who fires most as outliers across modes?
# Use per-mode outlier report to count anchor seeds
from collections import Counter
anchors = Counter()
outlier_df = pd.read_csv('out/programmatic-eda/compute-futures-2026-08-15/outlier_detector.csv')
print('=== outlier_detector counts ===')
print(outlier_df[['mode','column','outlier_count','outlier_pct']].to_string(index=False))
print()

# Padded vs unpadded seed contribution — recount ourselves per finding
# We need per-mode per-column IQR outlier rows
def iqr_outliers(x):
    q1, q3 = np.percentile(x, [25,75])
    iqr = q3-q1
    lo, hi = q1-1.5*iqr, q3+1.5*iqr
    return (x<lo) | (x>hi)

num_cols = ['role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs','x402Total','rounds','deniedWorkers']
outlier_positions = []
for m in df['mode'].unique():
    sub = df[df['mode']==m]
    for c in num_cols:
        if sub[c].nunique() <= 1:
            continue
        mask = iqr_outliers(sub[c].values)
        for _, row in sub[mask].iterrows():
            outlier_positions.append((m, c, int(row['seed']), row['role'], float(row[c])))

print(f'=== total outlier positions: {len(outlier_positions)} ===')

# Anchor seed count (which seeds appear in outlier positions?)
seed_counts = Counter([p[2] for p in outlier_positions])
print('Top 10 anchor seeds:')
for s, c in seed_counts.most_common(10):
    print(f'  seed={s} (len={len(str(s))}): {c} positions')

# Padded vs unpadded contribution
padded = sum(1 for p in outlier_positions if len(str(p[2]))==10)
unpadded = sum(1 for p in outlier_positions if len(str(p[2]))==9)
print(f'padded: {padded} ({100*padded/(padded+unpadded):.1f}%), unpadded: {unpadded} ({100*unpadded/(padded+unpadded):.1f}%)')

# Excluded seed-related outliers to compare with historical framing (non-wallet_sum_pnl positions)
non_wallet = [p for p in outlier_positions if p[1] != 'wallet_sum_pnl']
non_wallet_non_seed = [p for p in non_wallet if p[1] != 'seed']
padded_nw = sum(1 for p in non_wallet_non_seed if len(str(p[2]))==10)
unpadded_nw = sum(1 for p in non_wallet_non_seed if len(str(p[2]))==9)
print(f'non-wallet non-seed padded: {padded_nw} ({100*padded_nw/(padded_nw+unpadded_nw):.1f}%), unpadded: {unpadded_nw}')
