import pandas as pd

df = pd.read_csv('out/programmatic-eda/compute-futures-2026-10-22/distributions_by_mode.csv')
df = df.rename(columns={'Unnamed: 0': 'column'})

print('--- wallet_sum_pnl per mode ---')
w = df[df['column'] == 'wallet_sum_pnl'][['mode', 'count', 'mean', 'std', 'min', 'max']]
print(w.to_string(index=False))
print()

print('--- role_pnl per mode ---')
r = df[df['column'] == 'role_pnl'][['mode', 'count', 'mean', 'std', 'min', 'max']]
print(r.to_string(index=False))
print()

print('--- realizedAbs per mode ---')
ra = df[df['column'] == 'realizedAbs'][['mode', 'count', 'mean', 'std', 'min', 'max']]
print(ra.to_string(index=False))
print()

print('--- x402Total per mode ---')
x4 = df[df['column'] == 'x402Total'][['mode', 'count', 'mean', 'std', 'min', 'max']]
print(x4.to_string(index=False))
print()

print('--- minSpot/maxSpot/minCurve/maxCurve mean per mode ---')
for col in ['minSpot', 'maxSpot', 'minCurve', 'maxCurve']:
    sub = df[df['column'] == col][['mode', 'mean', 'std']]
    sub.insert(0, 'col', col)
    print(sub.to_string(index=False))
    print()

print('--- Constant columns per mode (std==0) ---')
const = df[df['std'] == 0][['mode', 'column', 'mean']]
print(const.to_string(index=False))
