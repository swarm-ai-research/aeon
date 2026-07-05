import pandas as pd
import numpy as np

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-07-05.csv')

cols_check = ['role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs']
syn = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
x40 = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)
print('=== synthetic vs x402 max |diff| at role level ===')
for c in cols_check:
    diff = (syn[c] - x40[c]).abs().max()
    print(f'  {c}: {diff}')

x = df[df['mode']=='x402']['x402Total']
print()
print('=== x402Total in x402 mode ===')
print(f'  mean={x.mean():.4f} std={x.std():.4f} min={x.min():.4f} max={x.max():.4f} sum={x.sum():.4f}')

print()
print('=== max |r| per mode (top-3 pairs, excluding rounds/deniedWorkers/x402Total-when-zero) ===')
for m in sorted(df['mode'].unique()):
    sub = df[df['mode']==m].select_dtypes(include='number').drop(columns=['rounds','deniedWorkers'], errors='ignore')
    if 'x402Total' in sub.columns and (sub['x402Total']==0).all():
        sub = sub.drop(columns=['x402Total'])
    corr = sub.corr()
    mask = np.triu(np.ones(corr.shape, dtype=bool), k=1)
    stacked = corr.where(mask).stack().sort_values(key=abs, ascending=False)
    print(f'  {m}: top 3 |r| pairs')
    for (a,b), v in stacked.head(3).items():
        print(f'    {a} x {b} = {v:+.3f}')

print()
print('=== constant columns per mode (std=0) ===')
for m in sorted(df['mode'].unique()):
    sub = df[df['mode']==m].select_dtypes(include='number')
    consts = [c for c in sub.columns if sub[c].std()==0]
    print(f'  {m}: {consts}')

print()
print('=== spread realizedAbs range ===')
sp = df[df['mode']=='spread']
print(f"  realizedAbs mean={sp['realizedAbs'].mean():.2f} std={sp['realizedAbs'].std():.2f} min={sp['realizedAbs'].min():.2f} max={sp['realizedAbs'].max():.2f}")
print(f"  role_pnl    mean={sp['role_pnl'].mean():.2f} std={sp['role_pnl'].std():.2f} min={sp['role_pnl'].min():.2f} max={sp['role_pnl'].max():.2f}")
print()
print('=== seed digit distribution ===')
seed_digits = df['seed'].astype(str).str.len().value_counts().sort_index()
print(seed_digits)
