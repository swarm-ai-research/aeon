import pandas as pd, numpy as np
df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-08-25.csv')

print('=== basket/synth per-seed multiplier ===')
basket = df[df['mode']=='basket'].groupby('seed').first()
synth  = df[df['mode']=='synthetic'].groupby('seed').first()
for col in ['minSpot','maxSpot','minCurve','maxCurve','realizedAbs']:
    ratios = basket[col] / synth[col]
    print(f'  {col:12s} mean={ratios.mean():.6f}  std={ratios.std():.3e}  min={ratios.min():.6f}  max={ratios.max():.6f}')

print()
print('=== synth vs x402 max abs diff ===')
s = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
x = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)
for c in ['role_pnl','wallet_sum_pnl','minSpot','maxSpot','minCurve','maxCurve','realizedAbs','settlementLegs']:
    d = (s[c]-x[c]).abs().max()
    print(f'  {c:16s} max_abs_diff={d}')

print()
print('=== realizedAbs distribution ===')
for m in ['basket','synthetic','x402']:
    d = df[df['mode']==m]['realizedAbs']
    q1, q3 = d.quantile(0.25), d.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
    outliers = d[(d<lo)|(d>hi)]
    print(f'  {m:10s} n={len(d)} q1={q1:.4f} q3={q3:.4f} iqr={iqr:.4f} bounds=[{lo:.4f},{hi:.4f}] outliers={len(outliers)}')
    print(f'    outlier values (unique, rounded): {sorted(outliers.round(2).unique())}')

print()
print('=== Spread retail per-seed losses (sorted) ===')
sr = df[(df['mode']=='spread')&(df['role']=='retail')].sort_values('role_pnl')
print(sr[['seed','role_pnl']].to_string(index=False))
print(f'retail: mean={sr.role_pnl.mean():.2f} sum={sr.role_pnl.sum():.2f} std={sr.role_pnl.std():.2f}')
n_neg = (sr.role_pnl < 0).sum()
print(f'retail losing: {n_neg}/{len(sr)}')

print()
print('=== Top-5 spread role_pnl losses (all roles) ===')
sp = df[df['mode']=='spread'].sort_values('role_pnl').head(5)
print(sp[['seed','role','role_pnl']].to_string(index=False))
print()
print('=== Top-5 spread role_pnl gains ===')
sp = df[df['mode']=='spread'].sort_values('role_pnl',ascending=False).head(5)
print(sp[['seed','role','role_pnl']].to_string(index=False))

print()
print('=== spread role means ===')
print(df[df['mode']=='spread'].groupby('role')['role_pnl'].agg(['mean','std','min','max','sum']).round(2))

print()
print('=== x402Total distribution (x402 mode only) ===')
x402t = df[df['mode']=='x402']['x402Total']
print(f'  n={len(x402t)}  min={x402t.min():.4f}  max={x402t.max():.4f}  mean={x402t.mean():.4f}  std={x402t.std():.4f}  range={x402t.max()-x402t.min():.4f}')

print()
print('=== Outlier positions per seed (excluding wallet_sum_pnl float dust, excluding x402Total in x402, excluding role_pnl in synth/x402 mirror) ===')
import subprocess
# Just look at outlier rows in outliers_by_mode.csv
oc = pd.read_csv('out/programmatic-eda/compute-futures-2026-08-25/outliers_by_mode.csv')
# Look at each (mode, column) with outlier_pct >= 10 to find which seeds anchor
oc10 = oc[oc.outlier_pct >= 10]
print(oc10.to_string(index=False))

print()
print('=== Per-seed non-dust outlier position count ===')
seed_pos = {}
for _, row in oc10.iterrows():
    m, c = row['mode'], row['column']
    if c == 'wallet_sum_pnl': continue
    if c == 'x402Total' and m == 'x402': continue
    if c == 'role_pnl' and m in ('synthetic','x402'): continue
    if c == 'seed': continue
    d = df[df['mode']==m][c]
    q1, q3 = d.quantile(0.25), d.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
    sub = df[df['mode']==m]
    out_rows = sub[(sub[c]<lo)|(sub[c]>hi)]
    for s in out_rows['seed']:
        seed_pos.setdefault(s, 0)
        seed_pos[s] += 1
for s, c in sorted(seed_pos.items(), key=lambda x: -x[1]):
    print(f'  seed {s}: {c}')

print()
print('=== Constant-by-mode columns ===')
num_cols = df.select_dtypes(include='number').columns
for m in sorted(df['mode'].unique()):
    d = df[df['mode']==m][num_cols]
    consts = [c for c in num_cols if d[c].std() == 0]
    print(f'  {m}: {consts}')

print()
print('=== Padded seeds ===')
padded = df[df['seed'] > 202700000]  # 2026082410, 11, 12 are big numbers
print(f'  padded seed row count: {len(padded)}/{len(df)}')
print(f'  padded seed values: {sorted(padded.seed.unique().tolist())}')
