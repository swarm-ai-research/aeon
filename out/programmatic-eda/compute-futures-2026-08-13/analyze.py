import pandas as pd
df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-08-13.csv')

# spread mode by role
for role in ['retail','operator','analyst']:
    sub = df[(df['mode']=='spread') & (df['role']==role)]
    print(f'spread {role}: n={len(sub)} mean_pnl={sub["role_pnl"].mean():.2f} min={sub["role_pnl"].min():.2f} max={sub["role_pnl"].max():.2f}')
print()

# top 5 gains and losses overall
print('Top 5 gains:')
top = df.nlargest(5, 'role_pnl')[['seed','mode','role','role_pnl']]
print(top.to_string(index=False))
print()
print('Top 5 losses:')
bot = df.nsmallest(5, 'role_pnl')[['seed','mode','role','role_pnl']]
print(bot.to_string(index=False))
print()

# scale ratios
b = df[df['mode']=='basket']['realizedAbs'].mean()
s = df[df['mode']=='synthetic']['realizedAbs'].mean()
sp = df[df['mode']=='spread']['realizedAbs'].mean()
print(f'realizedAbs means: basket={b:.2f} synth={s:.2f} spread={sp:.2f}')
print(f'basket/synth ratio = {b/s:.3f}x')
print(f'spread/basket ratio = {sp/b:.3f}x')
print()

# settlementLegs distribution
print('settlementLegs by mode:')
print(df.groupby('mode')['settlementLegs'].describe())
low_legs = df[df['settlementLegs']<77][['seed','mode','role','settlementLegs']]
print(f'\nRows with settlementLegs<77: n={len(low_legs)}')
print(low_legs.to_string(index=False))
print()

# x402Total distribution
print('x402Total in x402 mode:')
x4 = df[df['mode']=='x402']['x402Total']
print(f'min={x4.min():.2f} max={x4.max():.2f} mean={x4.mean():.2f} std={x4.std():.2f}')

# per-mode conservation
print()
print('Conservation per mode:')
for m in ['basket','spread','synthetic','x402']:
    ws = df[df['mode']==m]['wallet_sum_pnl']
    print(f'  {m}: mean={ws.mean():.4e} std={ws.std():.4e} max|abs|={ws.abs().max():.4e}')
