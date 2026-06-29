import pandas as pd
df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-06-28.csv')
s = df[df['mode']=='spread']['settlementLegs']
print('spread settlementLegs:')
print('  values:', sorted(s.unique().tolist()))
print('  counts:', s.value_counts().to_dict())
print('  q1:', s.quantile(0.25), 'q3:', s.quantile(0.75), 'IQR:', s.quantile(0.75)-s.quantile(0.25))
syn = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
x402 = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)
print('synthetic vs x402 role-level equivalence:')
for c in ['role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs']:
    diff = (syn[c]-x402[c]).abs().max()
    print(f'  max |diff| in {c}: {diff}')
print()
xt = df[df['mode']=='x402']['x402Total']
print(f'x402Total in x402: min={xt.min():.2f} max={xt.max():.2f} mean={xt.mean():.2f} std={xt.std():.2f}')
print()
print('role_pnl per-mode summary:')
for m in sorted(df['mode'].unique()):
    rp = df[df['mode']==m]['role_pnl']
    print(f'  {m:>10}  mean={rp.mean():+.4f}  std={rp.std():.4f}  min={rp.min():+.4f}  max={rp.max():+.4f}')
print()
print('seeds:')
print(sorted(df['seed'].unique().tolist()))
print()
print('basket settlementLegs (yesterdays comparison):')
s = df[df['mode']=='basket']['settlementLegs']
print('  values:', sorted(s.unique().tolist()))
print('  counts:', s.value_counts().to_dict())
print('  q1:', s.quantile(0.25), 'q3:', s.quantile(0.75), 'IQR:', s.quantile(0.75)-s.quantile(0.25))
print()
print('Notable correlations (|r| in 0.6..0.8) within mode:')
for m in sorted(df['mode'].unique()):
    sub = df[df['mode']==m].select_dtypes('number')
    c = sub.corr()
    pairs = []
    for i, a in enumerate(c.columns):
        for b in c.columns[i+1:]:
            r = c.loc[a,b]
            if pd.notna(r) and 0.6 <= abs(r) < 0.8:
                pairs.append((a,b,r))
    print(f'  {m}: {pairs}')
