import pandas as pd
for d in ['2026-09-04', '2026-09-05', '2026-09-06']:
    df = pd.read_csv(f'memory/gitlawb-compute-futures-proofs/{d}.csv')
    x = df[df['mode'] == 'x402']
    cols = ['x402Total', 'realizedAbs', 'minSpot', 'maxSpot', 'minCurve', 'maxCurve', 'settlementLegs']
    c = x[cols].corr()['x402Total'].round(3)
    print(d)
    print(c.to_string())
    print()

for d in ['2026-09-04', '2026-09-05', '2026-09-06']:
    df = pd.read_csv(f'memory/gitlawb-compute-futures-proofs/{d}.csv')
    print(d, 'basket realizedAbs std (seed-level):',
          df[df['mode']=='basket'].groupby('seed')['realizedAbs'].first().std().round(4),
          '2.5x ratio std:',
          (df[df['mode']=='basket'].groupby('seed')['realizedAbs'].first() /
           df[df['mode']=='synthetic'].groupby('seed')['realizedAbs'].first()).std().round(6))
    print(d, 'basket maxCurve std (seed-level):',
          df[df['mode']=='basket'].groupby('seed')['maxCurve'].first().std().round(6),
          '2.5x maxCurve ratio std:',
          (df[df['mode']=='basket'].groupby('seed')['maxCurve'].first() /
           df[df['mode']=='synthetic'].groupby('seed')['maxCurve'].first()).std().round(6))
    print(d, 'basket minCurve std (seed-level):',
          df[df['mode']=='basket'].groupby('seed')['minCurve'].first().std().round(6))
