import pandas as pd
import numpy as np

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-10-17.csv')

print('=== Multiplier (basket vs synthetic) on raw simulation columns ===')
# These columns are per-seed/per-role but for synthetic vs basket should be a pure multiplier if the regime holds
for col in ['minSpot','maxSpot','minCurve','maxCurve','realizedAbs']:
    b = df[df['mode']=='basket'].groupby('seed')[col].mean()
    s = df[df['mode']=='synthetic'].groupby('seed')[col].mean()
    ratios = (b/s).dropna()
    print(col, 'mean=', ratios.mean(), 'std=', ratios.std(), 'min=', ratios.min(), 'max=', ratios.max(), 'n=', len(ratios))

print()
print('=== Per-seed basket:synth minSpot ratio (should be a single multiplier if locked) ===')
b_min = df[df['mode']=='basket'].groupby('seed')['minSpot'].first()
s_min = df[df['mode']=='synthetic'].groupby('seed')['minSpot'].first()
print(pd.DataFrame({'basket':b_min,'synth':s_min,'ratio':b_min/s_min}))

print()
print('=== All four basket vs synth ratios per-seed (should be identical if lock holds) ===')
r_min = df[df['mode']=='basket'].groupby('seed')['minSpot'].first() / df[df['mode']=='synthetic'].groupby('seed')['minSpot'].first()
r_max = df[df['mode']=='basket'].groupby('seed')['maxSpot'].first() / df[df['mode']=='synthetic'].groupby('seed')['maxSpot'].first()
r_minC = df[df['mode']=='basket'].groupby('seed')['minCurve'].first() / df[df['mode']=='synthetic'].groupby('seed')['minCurve'].first()
r_maxC = df[df['mode']=='basket'].groupby('seed')['maxCurve'].first() / df[df['mode']=='synthetic'].groupby('seed')['maxCurve'].first()
ratios = pd.DataFrame({'r_minSpot':r_min,'r_maxSpot':r_max,'r_minCurve':r_minC,'r_maxCurve':r_maxC})
print(ratios)
print()
print('unique r_minSpot:', sorted(ratios['r_minSpot'].round(6).unique()))
print('unique r_maxSpot:', sorted(ratios['r_maxSpot'].round(6).unique()))

print()
print('=== Spread retail stats ===')
spread = df[df['mode']=='spread']
sr = spread[spread['role']=='retail']
sa = spread[spread['role']=='analyst']
so = spread[spread['role']=='operator']
print('retail  mean=', sr['role_pnl'].mean(), 'min=', sr['role_pnl'].min(), 'max=', sr['role_pnl'].max())
print('analyst mean=', sa['role_pnl'].mean(), 'min=', sa['role_pnl'].min(), 'max=', sa['role_pnl'].max())
print('operator mean=', so['role_pnl'].mean(), 'min=', so['role_pnl'].min(), 'max=', so['role_pnl'].max())
print('spread realizedAbs mean=', spread['realizedAbs'].mean())

print()
print('=== Top-6 spread losses by role ===')
print(spread.nsmallest(6, 'role_pnl')[['seed','role','role_pnl']])

print()
print('=== Top-6 spread gains by role ===')
print(spread.nlargest(6, 'role_pnl')[['seed','role','role_pnl']])

print()
print('=== Padded seeds (10-digit) in spread top-6 losses ===')
top6_loss = spread.nsmallest(6, 'role_pnl')
padded_mask = top6_loss['seed'].astype(str).str.len() == 10
print('padded in top-6 losses:', padded_mask.sum(), 'of 6')
print('padded seeds:', sorted(top6_loss[padded_mask]['seed'].tolist()))

print()
print('=== minSpot x maxSpot per-mode (excluding padded seeds) ===')
nonpad = df[df['seed'].astype(str).str.len() == 9]
for m in sorted(df['mode'].unique()):
    sub = nonpad[nonpad['mode']==m]
    if len(sub) > 1:
        r = sub['minSpot'].corr(sub['maxSpot'])
        print(f'{m}: minSpot x maxSpot = {r:.3f}')

print()
print('=== synthetic vs x402 role-level identity (max abs diff) ===')
cols_shared = ['role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs']
syn = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
x = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)
diffs = {c: float((syn[c] - x[c]).abs().max()) for c in cols_shared}
print(diffs)

print()
print('=== x402Total range in x402 mode ===')
xmode = df[df['mode']=='x402']['x402Total']
print('min=', xmode.min(), 'max=', xmode.max(), 'mean=', xmode.mean(), 'std=', xmode.std(), 'range=', xmode.max()-xmode.min())

print()
print('=== All highest within-mode non-trivial correlations (|r|>=0.5) ===')
for m in sorted(df['mode'].unique()):
    sub = df[df['mode']==m]
    numeric = sub.select_dtypes(include=[np.number]).drop(columns=['seed'], errors='ignore')
    numeric = numeric.loc[:, numeric.std() > 1e-6]
    cm = numeric.corr()
    seen = set()
    pairs = []
    for a in cm.index:
        for b in cm.columns:
            if a==b: continue
            if (b,a) in seen: continue
            r = cm.loc[a,b]
            if pd.notna(r) and abs(r) >= 0.5:
                seen.add((a,b))
                pairs.append((abs(r), a, b, r))
    pairs.sort(reverse=True)
    print(f'{m}:')
    for _, a, b, r in pairs[:6]:
        print(f'  {a} x {b}: r={r:.3f}')
