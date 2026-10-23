import pandas as pd

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-10-22.csv')

# Confirm top-N analysis in x402
x = df[df['mode'] == 'x402']
print('--- x402Total per seed ---')
print(x.groupby('seed')['x402Total'].first().sort_values().to_string())
print()
print('x402Total mean/std/min/max/range:')
print(f'  mean={x["x402Total"].mean():.2f}  std={x["x402Total"].std():.2f}')
print(f'  min={x["x402Total"].min():.2f}  max={x["x402Total"].max():.2f}  range={x["x402Total"].max() - x["x402Total"].min():.2f}')

# Compare spread's maxCurve x seed under padded vs not
print()
print('--- spread maxCurve x seed correlations ---')
sp = df[df['mode'] == 'spread']
print(f'  all: {sp["maxCurve"].corr(sp["seed"]):.3f}')
non_pad = sp[sp['seed'] <= 1e9]
pad = sp[sp['seed'] > 1e9]
print(f'  non-padded (n={len(non_pad)}): {non_pad["maxCurve"].corr(non_pad["seed"]):.3f}')
print(f'  padded (n={len(pad)}): {pad["maxCurve"].corr(pad["seed"]):.3f}')

# Spread's realizedAbs x maxCurve (noted as 0.706)
print(f'  spread realizedAbs x maxCurve: {sp["realizedAbs"].corr(sp["maxCurve"]):.3f}')

# Settlement + spotSource
print()
print('--- settlement / spotSource per mode ---')
for m in ['basket', 'spread', 'synthetic', 'x402']:
    sub = df[df['mode'] == m]
    print(f'  {m}: settlement={sorted(sub["settlement"].unique().tolist())}  spotSource={sorted(sub["spotSource"].unique().tolist())}  live={sorted(sub["live"].unique().tolist())}')

# Sign pattern per mode wallet_sum_pnl (mean > 0, < 0, == 0)
print()
print('--- wallet_sum_pnl mean sign per mode ---')
for m in ['basket', 'spread', 'synthetic', 'x402']:
    mu = df[df['mode'] == m]['wallet_sum_pnl'].mean()
    sign = 'POS' if mu > 0 else ('NEG' if mu < 0 else 'ZERO')
    print(f'  {m}: mean={mu:e} ({sign})')
