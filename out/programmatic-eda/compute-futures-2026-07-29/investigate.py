import pandas as pd

raw = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-07-29.csv')

# Investigate minCurve/maxCurve distribution per mode
for m in raw['mode'].unique():
    for col in ['minCurve', 'maxCurve', 'settlementLegs']:
        v = raw[raw['mode'] == m][col]
        vc = v.value_counts().sort_index()
        print(f'{m}/{col}: n_unique={v.nunique()}, values={dict(vc)}')
    print()

# Compare with 07-28 (prior day)
print('=== 07-28 minCurve/maxCurve per mode ===')
prior = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-07-28.csv')
for m in prior['mode'].unique():
    for col in ['minCurve', 'maxCurve', 'settlementLegs']:
        v = prior[prior['mode'] == m][col]
        vc = v.value_counts().sort_index()
        print(f'{m}/{col}: n_unique={v.nunique()}, values={dict(vc)}')
    print()

# x402 settlementLegs × x402Total correlation history recheck
print('=== 07-29 x402 correlations ===')
x = raw[raw['mode'] == 'x402']
corr = x[['seed', 'role_pnl', 'wallet_sum_pnl', 'realizedAbs', 'minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'settlementLegs', 'x402Total']].corr()
print(f'settlementLegs × x402Total: {corr.loc["settlementLegs", "x402Total"]:.3f}')
print(f'minSpot × x402Total: {corr.loc["minSpot", "x402Total"]:.3f}')
print(f'realizedAbs × x402Total: {corr.loc["realizedAbs", "x402Total"]:.3f}')
print(f'wallet_sum_pnl × x402Total: {corr.loc["wallet_sum_pnl", "x402Total"]:.3f}')
print(f'minCurve × x402Total: {corr.loc["minCurve", "x402Total"]:.3f}')

# check if the -0.596 basket seed × settlementLegs is real
print()
print('=== basket seed correlations ===')
b = raw[raw['mode'] == 'basket']
bcorr = b[['seed', 'role_pnl', 'realizedAbs', 'minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'settlementLegs']].corr()
print(f'seed × settlementLegs: {bcorr.loc["seed", "settlementLegs"]:.3f}')

# check spread wallet_sum_pnl vs 07-28
print()
print('=== spread wallet_sum_pnl trend ===')
for date in ['2026-07-25', '2026-07-28', '2026-07-29']:
    try:
        pdf = pd.read_csv(f'memory/gitlawb-compute-futures-proofs/{date}.csv')
        s = pdf[pdf['mode'] == 'spread']['wallet_sum_pnl']
        print(f'{date}: mean={s.mean():.3e}, std={s.std():.3e}, absmax={s.abs().max():.3e}, range={s.max()-s.min():.3e}')
    except Exception as e:
        print(f'{date}: {e}')

# maxSpot single-seed anchor check for 07-29 (compare to 07-28's seed 202607286)
print()
print('=== maxSpot top seed 07-29 ===')
for m in raw['mode'].unique():
    s = raw[raw['mode'] == m].nlargest(2, 'maxSpot')[['seed', 'maxSpot']].drop_duplicates()
    print(f'{m}:')
    print(s.to_string(index=False))

# x402Total trend
print()
print('=== x402Total trend ===')
for date in ['2026-07-24', '2026-07-25', '2026-07-28', '2026-07-29']:
    try:
        pdf = pd.read_csv(f'memory/gitlawb-compute-futures-proofs/{date}.csv')
        s = pdf[pdf['mode'] == 'x402']['x402Total']
        print(f'{date}: mean={s.mean():.2f}, min={s.min():.2f}, max={s.max():.2f}, range={s.max()-s.min():.2f}, sum={s.sum():.2f}')
    except Exception as e:
        print(f'{date}: {e}')
