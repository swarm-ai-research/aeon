import pandas as pd
df = pd.read_csv('out/programmatic-eda/compute-futures-2026-06-08/sweep_dedup.csv')
print('=== mode x live x spotSource cross ===')
print(df.groupby(['mode','live','spotSource']).size())
print('\n=== mode x settlement ===')
print(df.groupby(['mode','settlement']).size())
print('\n=== role distribution per mode ===')
print(df.groupby(['mode','role']).size())

print('\n=== role_pnl by mode x role (mean, std) ===')
g = df.groupby(['mode','role'])['role_pnl'].agg(['mean','std','min','max'])
print(g.to_string())

# x402 totals
print('\n=== x402 mode x402Total stats ===')
x = df[df['mode']=='x402']['x402Total']
print(f'sum={x.sum():.2f} mean={x.mean():.2f} min={x.min():.2f} max={x.max():.2f} count={len(x)}')

# synthetic vs x402 role-pnl identity check
print('\n=== synthetic vs x402 role_pnl identity ===')
syn = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
x4 = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)
diff = (syn['role_pnl'] - x4['role_pnl']).abs().max()
print(f'max |diff| across {len(syn)} paired rows: {diff}')
