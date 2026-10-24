import pandas as pd
import numpy as np

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-10-23.csv')
print('Row count:', len(df))
print('Modes:', sorted(df['mode'].unique().tolist()))
print('Seeds per mode:', df.groupby('mode')['seed'].nunique().to_dict())
print('All unique seeds:', sorted(df['seed'].unique().tolist()))
print()

# Multiplier: basket vs synth price ratio
for col in ['minSpot','maxSpot','minCurve','maxCurve']:
    bb = df[df['mode']=='basket'][['seed','role',col]].rename(columns={col:'b'})
    ss = df[df['mode']=='synthetic'][['seed','role',col]].rename(columns={col:'s'})
    merged = bb.merge(ss, on=['seed','role'])
    ratios = merged['b']/merged['s']
    print(f'{col}: basket/synth ratio mean={ratios.mean():.6f} std={ratios.std():.2e} min={ratios.min():.6f} max={ratios.max():.6f}')
print()

# x402Total analysis
x402 = df[df['mode']=='x402']
print(f'x402Total mean=${x402["x402Total"].mean():.2f} std=${x402["x402Total"].std():.2f} min=${x402["x402Total"].min():.2f} max=${x402["x402Total"].max():.2f}')
print(f'x402Total range: ${x402["x402Total"].max()-x402["x402Total"].min():.2f}')
print()

# Padded seed detection: seeds like 2026102210, 2026102211, 2026102212 are 10 digits; others are 9
seed_lengths = df['seed'].astype(str).str.len()
print('Seed length distribution:', seed_lengths.value_counts().to_dict())
padded_mask = df['seed'].astype(str).str.len() >= 10
print(f'Padded seeds ({padded_mask.sum()} rows):', sorted(df[padded_mask]['seed'].unique().tolist()))
print(f'Non-padded seeds ({(~padded_mask).sum()} rows):', sorted(df[~padded_mask]['seed'].unique().tolist()))
print()

# x402Total by padded/non-padded
x402_padded = x402[x402['seed'].astype(str).str.len() >= 10]
x402_nonpadded = x402[x402['seed'].astype(str).str.len() < 10]
print(f'x402Total non-padded mean=${x402_nonpadded["x402Total"].mean():.2f} std=${x402_nonpadded["x402Total"].std():.2f} range=${x402_nonpadded["x402Total"].max()-x402_nonpadded["x402Total"].min():.2f}')
print(f'x402Total padded mean=${x402_padded["x402Total"].mean():.2f} std=${x402_padded["x402Total"].std():.2f} range=${x402_padded["x402Total"].max()-x402_padded["x402Total"].min():.2f}')
# Top 3 x402Total values
print('Top 3 x402Total rows:')
print(x402.nlargest(3, 'x402Total')[['seed','role','x402Total']])
print()

# Spread retail top-6 losses
spread = df[df['mode']=='spread']
print('Spread role means:')
print(spread.groupby('role')['role_pnl'].agg(['mean','std','min','max']))
print()
print('Spread top-6 losses:')
top_losses = spread.nsmallest(6, 'role_pnl')[['seed','role','role_pnl']]
print(top_losses)
print(f'Padded in top-6 losses: {(top_losses["seed"].astype(str).str.len() >= 10).sum()}/6')
print(f'Retail in top-6 losses: {(top_losses["role"]=="retail").sum()}/6')
print()
print('Spread top-6 gains:')
print(spread.nlargest(6, 'role_pnl')[['seed','role','role_pnl']])
print()

# Spread retail padded vs non-padded
spread_retail = spread[spread['role']=='retail']
spread_retail_padded = spread_retail[spread_retail['seed'].astype(str).str.len() >= 10]
spread_retail_nonpadded = spread_retail[spread_retail['seed'].astype(str).str.len() < 10]
print(f'Spread retail padded mean=${spread_retail_padded["role_pnl"].mean():.2f}')
print(f'Spread retail non-padded mean=${spread_retail_nonpadded["role_pnl"].mean():.2f}')
if abs(spread_retail_nonpadded['role_pnl'].mean()) > 0:
    ratio = spread_retail_padded['role_pnl'].mean() / spread_retail_nonpadded['role_pnl'].mean()
    print(f'Padded/non-padded ratio: {ratio:.3f}')
print()

# minSpot x maxSpot correlation per mode (within-mode non-padded)
print('minSpot × maxSpot correlation per mode:')
for m in sorted(df['mode'].unique()):
    sub = df[df['mode']==m]
    sub_np = sub[sub['seed'].astype(str).str.len() < 10]
    r_all = sub[['minSpot','maxSpot']].corr().iloc[0,1]
    r_np = sub_np[['minSpot','maxSpot']].corr().iloc[0,1]
    print(f'  {m}: all={r_all:+.3f}  non-padded={r_np:+.3f}')
print()

# Conservation check per mode
print('wallet_sum_pnl per mode:')
for m in sorted(df['mode'].unique()):
    sub = df[df['mode']==m]
    print(f'  {m}: mean={sub["wallet_sum_pnl"].mean():+.3e}  std={sub["wallet_sum_pnl"].std():.3e}  min={sub["wallet_sum_pnl"].min():+.3e}  max={sub["wallet_sum_pnl"].max():+.3e}')
print()

# synthetic vs x402 identity check
syn = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
xf = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)
shared_cols = ['role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs']
max_diff = 0.0
for c in shared_cols:
    d = (syn[c] - xf[c]).abs().max()
    if d > max_diff:
        max_diff = d
print(f'synth vs x402 max abs diff across {len(shared_cols)} shared cols: {max_diff:.3e}')
print()

# Row/col shape
print(f'Shape: {df.shape[0]} rows × {df.shape[1]} cols')
print(f'rounds unique: {df["rounds"].unique()}')
print(f'deniedWorkers unique: {df["deniedWorkers"].unique()}')
print(f'live by mode: {df.groupby("mode")["live"].unique().to_dict()}')
print(f'settlement by mode: {df.groupby("mode")["settlement"].unique().to_dict()}')
print(f'spotSource by mode: {df.groupby("mode")["spotSource"].unique().to_dict()}')
