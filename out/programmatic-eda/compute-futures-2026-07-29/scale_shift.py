import pandas as pd

for date in ['2026-07-24', '2026-07-25', '2026-07-27', '2026-07-28', '2026-07-29']:
    try:
        d = pd.read_csv(f'memory/gitlawb-compute-futures-proofs/{date}.csv')
        print(f'=== {date} (basket) ===')
        b = d[d['mode'] == 'basket']
        for c in ['minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'realizedAbs']:
            print(f'  {c}: mean={b[c].mean():.4f}, min={b[c].min():.4f}, max={b[c].max():.4f}, span={b[c].max()-b[c].min():.4f}')

        print(f'=== {date} (synthetic) ===')
        s = d[d['mode'] == 'synthetic']
        for c in ['minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'realizedAbs']:
            print(f'  {c}: mean={s[c].mean():.4f}, min={s[c].min():.4f}, max={s[c].max():.4f}, span={s[c].max()-s[c].min():.4f}')

        print(f'=== {date} (spread) ===')
        sp = d[d['mode'] == 'spread']
        for c in ['minSpot', 'maxSpot', 'minCurve', 'maxCurve']:
            print(f'  {c}: mean={sp[c].mean():.2f}, min={sp[c].min():.2f}, max={sp[c].max():.2f}, span={sp[c].max()-sp[c].min():.2f}')
        print()
    except Exception as e:
        print(f'{date}: {e}')

# Check role_pnl scale trajectory
print('=== role_pnl scale trajectory ===')
for date in ['2026-07-24', '2026-07-25', '2026-07-27', '2026-07-28', '2026-07-29']:
    d = pd.read_csv(f'memory/gitlawb-compute-futures-proofs/{date}.csv')
    for m in ['basket', 'spread', 'synthetic']:
        r = d[d['mode'] == m]['role_pnl']
        print(f'  {date} {m}: mean={r.mean():.2f}, std={r.std():.2f}')
