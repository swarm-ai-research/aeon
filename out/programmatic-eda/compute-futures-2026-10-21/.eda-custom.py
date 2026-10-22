import pandas as pd

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-10-21.csv')
print('=== Rows per mode x role ===')
print(df.groupby(['mode','role']).size())
print()
print('=== Multiplier basket:synth per-seed per-column (precise) ===')
cols = ['minSpot','maxSpot','minCurve','maxCurve']
for col in cols:
    bk = df[df['mode']=='basket'].groupby('seed')[col].mean()
    sy = df[df['mode']=='synthetic'].groupby('seed')[col].mean()
    r = bk/sy
    print(f'{col}: mean_ratio={r.mean():.6f} std={r.std():.2e} min={r.min():.6f} max={r.max():.6f}')
print()
print('=== Modes/role role_pnl means ===')
print(df.groupby(['mode','role'])['role_pnl'].agg(['count','mean','sum']))
print()
print('=== x402Total x402 mode ===')
x = df[df['mode']=='x402']['x402Total']
print('mean=', round(x.mean(),4), 'std=', round(x.std(),4), 'min=', round(x.min(),4), 'max=', round(x.max(),4), 'range=', round(x.max()-x.min(),4))
print()
print('=== synth vs x402 identity (max abs diff per column) ===')
sy = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
x4 = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)
for col in ['role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs']:
    diff = (sy[col] - x4[col]).abs().max()
    print(f'  {col}: {diff:.2e}')
print()
print('=== Spread top-6 losses ===')
sp = df[df['mode']=='spread'].sort_values('role_pnl').head(6)
print(sp[['seed','role','role_pnl']].to_string(index=False))
print()
print('=== Spread top-6 gains ===')
sg = df[df['mode']=='spread'].sort_values('role_pnl', ascending=False).head(6)
print(sg[['seed','role','role_pnl']].to_string(index=False))
print()
print('=== Spread per-role mean role_pnl ===')
print(df[df['mode']=='spread'].groupby('role')['role_pnl'].mean())
print()
print('=== min x maxSpot correlation per mode ===')
for m in sorted(df['mode'].unique()):
    r = df[df['mode']==m][['minSpot','maxSpot']].corr().iloc[0,1]
    print(f'  {m}: {r:+.4f}')
print()
print('=== Padded seeds (10-digit) check ===')
padded_mask = df['seed'].astype(str).str.len() > 9
print('padded seed values:', sorted(df[padded_mask]['seed'].unique().tolist()))
print('counts per mode (padded):')
print(df[padded_mask].groupby('mode').size())
print('spread retail padded mean:', df[(df['mode']=='spread')&padded_mask&(df['role']=='retail')]['role_pnl'].mean())
print('spread retail non-padded mean:', df[(df['mode']=='spread')&~padded_mask&(df['role']=='retail')]['role_pnl'].mean())
print('ratio padded/non-padded:', df[(df['mode']=='spread')&padded_mask&(df['role']=='retail')]['role_pnl'].mean() / df[(df['mode']=='spread')&~padded_mask&(df['role']=='retail')]['role_pnl'].mean())
print()
print('=== Conservation sign pattern ===')
for m in sorted(df['mode'].unique()):
    v = df[df['mode']==m]['wallet_sum_pnl']
    print(f'  {m}: mean={v.mean():+.3e} std={v.std():.3e} sign={"+" if v.mean()>=0 else "-"}')
print()
print('=== Constants/by-design check ===')
for col in ['rounds','deniedWorkers']:
    print(f'  {col} unique: {df[col].unique().tolist()}')
print('  live by mode:')
print(df.groupby('mode')['live'].agg(lambda s: s.unique().tolist()))
print('  settlement by mode:')
print(df.groupby('mode')['settlement'].agg(lambda s: s.unique().tolist()))
print('  spotSource by mode:')
print(df.groupby('mode')['spotSource'].agg(lambda s: s.unique().tolist()))
