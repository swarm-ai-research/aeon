import pandas as pd

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-06-20.csv')

print('=== Per-mode conservation: wallet_sum_pnl ===')
agg = df.groupby('mode')['wallet_sum_pnl'].agg(['mean', 'std', 'min', 'max', 'count']).reset_index()
print(agg.to_string(index=False))

print('\n=== role_pnl per mode ===')
pnl = df.groupby('mode')['role_pnl'].agg(['mean', 'std', 'min', 'max']).reset_index()
print(pnl.to_string(index=False))

print('\n=== x402Total per mode ===')
x = df.groupby('mode')['x402Total'].agg(['mean', 'std', 'min', 'max']).reset_index()
print(x.to_string(index=False))

print('\n=== realizedAbs per mode ===')
r = df.groupby('mode')['realizedAbs'].agg(['mean', 'std', 'min', 'max']).reset_index()
print(r.to_string(index=False))

print('\n=== role_pnl by mode and role ===')
prr = df.groupby(['mode', 'role'])['role_pnl'].agg(['mean', 'std', 'min', 'max']).reset_index()
print(prr.to_string(index=False))

print('\n=== synthetic vs x402 role_pnl equality check (same seed/role) ===')
syn = df[df['mode'] == 'synthetic'].set_index(['seed', 'role'])['role_pnl']
x402 = df[df['mode'] == 'x402'].set_index(['seed', 'role'])['role_pnl']
joined = pd.concat([syn.rename('synthetic'), x402.rename('x402')], axis=1).dropna()
joined['diff'] = (joined['synthetic'] - joined['x402']).abs()
print(f'count: {len(joined)}, max abs diff: {joined["diff"].max()}')

print('\n=== denied/rounds/live/settlement/spotSource ===')
print('deniedWorkers:', df['deniedWorkers'].unique().tolist())
print('rounds:', df['rounds'].unique().tolist())
print('live by mode:')
print(df.groupby(['mode', 'live']).size())
print('settlement by mode:')
print(df.groupby(['mode', 'settlement']).size())
print('spotSource by mode:')
print(df.groupby(['mode', 'spotSource']).size())

print('\n=== seeds ===')
print('unique seeds:', sorted(df['seed'].unique().tolist()))

print('\n=== conservation drift gate (mean>10 OR std>100) ===')
for mode, sub in df.groupby('mode'):
    m = sub['wallet_sum_pnl'].mean()
    s = sub['wallet_sum_pnl'].std()
    flag = (abs(m) > 10) or (s > 100)
    print(f'  {mode}: mean={m:.3e}, std={s:.3e}, drift={flag}')
