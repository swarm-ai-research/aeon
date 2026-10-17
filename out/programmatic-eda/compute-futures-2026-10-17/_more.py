import pandas as pd
import numpy as np

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-10-17.csv')

print('=== Padded vs non-padded spread retail mean/count ===')
spread_retail = df[(df['mode']=='spread') & (df['role']=='retail')].copy()
spread_retail['padded'] = spread_retail['seed'].astype(str).str.len() == 10
print(spread_retail.groupby('padded')['role_pnl'].agg(['count','mean','min','max']))

print()
print('=== All padded seeds in spread (any role) tail positions ===')
spread = df[df['mode']=='spread']
spread_sorted = spread.sort_values('role_pnl')
print('Top-10 losses:')
print(spread_sorted.head(10)[['seed','role','role_pnl']])
print('Top-10 gains:')
print(spread_sorted.tail(10)[['seed','role','role_pnl']])

print()
print('=== basket vs synthetic role_pnl check ===')
# synthetic ≡ x402 at role level; what about basket:synth multiplier at role_pnl level?
b = df[df['mode']=='basket'].sort_values(['seed','role']).reset_index(drop=True)
s = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
rp_ratio = (b['role_pnl']/s['role_pnl'])
print('basket/synth role_pnl ratio stats:')
print(rp_ratio.describe())
print('Max abs dev from 2.19375:', (rp_ratio - 2.19375).abs().max())

print()
print('=== Comparison values ===')
# Hypothesis: basket role_pnl = (basket spot & curve under 2.19375 mult, same stochastics) so role_pnl ratios should also sit near 2.19375 but not exactly because the P&L calc is non-linear in minSpot/maxSpot.
# Not a bug, just a note.
print('role_pnl ratio median:', rp_ratio.median(), 'mean:', rp_ratio.mean())

print()
print('=== Highest-correlation within-mode pairs (|r| non-trivial) ===')
# Already in previous script
print()
print('=== Seed-encoding artifact: padded seed count ===')
print(df['seed'].astype(str).str.len().value_counts())
# 9-digit vs 10-digit split per mode
tmp = df.copy()
tmp['digit'] = tmp['seed'].astype(str).str.len()
print(tmp.groupby('mode')['digit'].value_counts())
