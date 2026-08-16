"""Identify specific anchor seeds for each per-mode outlier cluster."""
import pandas as pd
import numpy as np
from collections import Counter

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-08-15.csv')

def iqr_outliers(x):
    q1, q3 = np.percentile(x, [25,75])
    iqr = q3-q1
    lo, hi = q1-1.5*iqr, q3+1.5*iqr
    return (x<lo) | (x>hi), lo, hi

num_cols = ['role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs','x402Total']

# For each per-mode column with outliers, list the anchor rows
print('=== ANCHOR DETAILS per (mode, column) ===')
outlier_positions = []
for m in ['basket','spread','synthetic','x402']:
    sub = df[df['mode']==m].copy()
    for c in num_cols:
        if sub[c].nunique() <= 1:
            continue
        mask, lo, hi = iqr_outliers(sub[c].values)
        if mask.sum() == 0:
            continue
        anchors = sub[mask].groupby('seed').size().to_dict()
        rows = sub[mask]
        # Distinguish LOW/HIGH
        low_rows = rows[rows[c] < lo]
        high_rows = rows[rows[c] > hi]
        # Get anchor seeds LOW/HIGH
        low_seeds = sorted(low_rows['seed'].unique().tolist())
        high_seeds = sorted(high_rows['seed'].unique().tolist())
        print(f'{m} {c}: n={mask.sum()} outliers, fence=[{lo:.4f}, {hi:.4f}]')
        print(f'  LOW anchors (seeds): {low_seeds}, vals: {sorted(low_rows[c].round(4).unique().tolist())}')
        print(f'  HIGH anchors (seeds): {high_seeds}, vals: {sorted(high_rows[c].round(4).unique().tolist())}')
        # Anchor concentration
        for seed, n in sorted(anchors.items(), key=lambda x: -x[1]):
            print(f'    seed={seed}: {n} row positions')
        for _, row in rows.iterrows():
            outlier_positions.append((m, c, int(row['seed']), row['role'], float(row[c])))
print()

# Cross-mode anchor concentration excluding seed column
print('=== Cross-mode anchor concentration (excluding seed column) ===')
seed_multi = Counter([p[2] for p in outlier_positions])
for s, c in seed_multi.most_common(15):
    modes_hit = set()
    cols_hit = set()
    for m, col, sd, r, v in outlier_positions:
        if sd == s:
            modes_hit.add(m)
            cols_hit.add(col)
    print(f'  seed={s} (len={len(str(s))}): {c} positions, modes={sorted(modes_hit)}, cols={sorted(cols_hit)}')

# Padded vs unpadded contribution (excl seed column)
padded = sum(1 for p in outlier_positions if len(str(p[2]))==10)
unpadded = sum(1 for p in outlier_positions if len(str(p[2]))==9)
print(f'\nExcluding seed column: padded={padded} ({100*padded/(padded+unpadded):.1f}%), unpadded={unpadded} ({100*unpadded/(padded+unpadded):.1f}%)')
print(f'Total non-seed non-wallet_sum_pnl positions used for padding check: {padded+unpadded}')
