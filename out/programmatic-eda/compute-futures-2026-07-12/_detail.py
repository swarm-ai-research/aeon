import pandas as pd
df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-07-12.csv')
x402 = df[df['mode']=='x402']
print(f'x402 rows: {len(x402)}')
print(f'x402Total sum: {x402["x402Total"].sum():.2f}')
print(f'x402Total mean: {x402["x402Total"].mean():.4f}')
print(f'x402Total max: {x402["x402Total"].max():.4f}')
print(f'x402Total min: {x402["x402Total"].min():.4f}')
print()

syn = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
x40 = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)
for c in ['role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs']:
    d = (syn[c].values - x40[c].values)
    print(f'{c}: max|diff|={abs(d).max()}')
print()

sp = df[df['mode']=='spread']
print('spread settlementLegs distribution:')
print(sp['settlementLegs'].value_counts().sort_index())
print(f'IQR: q25={sp["settlementLegs"].quantile(0.25)} q75={sp["settlementLegs"].quantile(0.75)}')
print(f'mean={sp["settlementLegs"].mean():.4f} std={sp["settlementLegs"].std():.4f} min={sp["settlementLegs"].min()} max={sp["settlementLegs"].max()}')
print()

print('seed by digit count:')
print(df['seed'].apply(lambda x: len(str(x))).value_counts())
print()

# key correlations to track from prior report
for m in ['basket','spread','synthetic','x402']:
    sub = df[df['mode']==m]
    if 'wallet_sum_pnl' in sub.columns and len(sub)>0:
        try:
            r_wallet_settle = sub[['wallet_sum_pnl','settlementLegs']].corr().iloc[0,1]
        except Exception:
            r_wallet_settle = float('nan')
        try:
            r_realized_wallet = sub[['realizedAbs','wallet_sum_pnl']].corr().iloc[0,1]
        except Exception:
            r_realized_wallet = float('nan')
        print(f'{m}: wallet_sum_pnl x settlementLegs = {r_wallet_settle:.3f}, realizedAbs x wallet_sum_pnl = {r_realized_wallet:.3f}')

# x402 wallet_sum_pnl x x402Total
x_sub = df[df['mode']=='x402']
r = x_sub[['wallet_sum_pnl','x402Total']].corr().iloc[0,1]
print(f'x402: wallet_sum_pnl x x402Total = {r:.3f}')
# x402 spot/curve x x402Total
for c in ['minSpot','maxSpot','minCurve','maxCurve','settlementLegs']:
    r = x_sub[[c,'x402Total']].corr().iloc[0,1]
    print(f'x402: {c} x x402Total = {r:.3f}')

# yesterday's row/col count vs today
prior = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-07-10.csv')
print(f'\nPrior (07-10): {len(prior)} rows, {len(prior.columns)} cols, modes={sorted(prior["mode"].unique())}')
print(f'Today (07-12): {len(df)} rows, {len(df.columns)} cols, modes={sorted(df["mode"].unique())}')
print(f'Column diff: added={set(df.columns)-set(prior.columns)}, removed={set(prior.columns)-set(df.columns)}')
