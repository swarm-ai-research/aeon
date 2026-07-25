import pandas as pd
df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-07-25.csv')

b = df[df['mode']=='basket']['settlementLegs'].value_counts().sort_index()
print('basket settlementLegs dist:', b.to_dict())

s = df[df['mode']=='spread'][['seed','maxSpot']].drop_duplicates('seed').sort_values('maxSpot')
print('spread maxSpot per seed:')
print(s.to_string(index=False))

# 07-25 spread minSpot per seed
sm = df[df['mode']=='spread'][['seed','minSpot']].drop_duplicates('seed').sort_values('minSpot')
print('spread minSpot per seed:')
print(sm.to_string(index=False))

# basket realizedAbs per seed (unique)
br = df[df['mode']=='basket'][['seed','realizedAbs']].drop_duplicates('seed').sort_values('realizedAbs')
print('basket realizedAbs per seed:')
print(br.to_string(index=False))

# Corr check per mode: near-threshold pairs (|r| between 0.5 and 0.8) excluding wallet_sum_pnl
for mode in df['mode'].unique():
    sub = df[df['mode']==mode].select_dtypes(include='number').drop(columns=['rounds','deniedWorkers'], errors='ignore')
    corr = sub.corr()
    pairs = []
    cols = list(corr.columns)
    for i, a in enumerate(cols):
        for b in cols[i+1:]:
            r = corr.loc[a,b]
            if pd.notna(r) and abs(r) >= 0.5 and a != 'wallet_sum_pnl' and b != 'wallet_sum_pnl':
                pairs.append((a,b,round(r,3)))
    pairs.sort(key=lambda x: -abs(x[2]))
    print(f'\n{mode} near-threshold pairs (excluding wallet_sum_pnl):')
    for p in pairs[:8]:
        print(f'  {p[0]} × {p[1]} = {p[2]:+.3f}')

# spread wallet_sum_pnl absolute range
sw = df[df['mode']=='spread']['wallet_sum_pnl']
print(f'\nspread wallet_sum_pnl: min={sw.min():.3e} max={sw.max():.3e} absmax={sw.abs().max():.3e} range={sw.max()-sw.min():.3e}')
