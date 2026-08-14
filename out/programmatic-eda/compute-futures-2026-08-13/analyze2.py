import pandas as pd
df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-08-13.csv')

# basket/synth ratio per seed for maxSpot minSpot maxCurve minCurve realizedAbs
b = df[df['mode']=='basket'].set_index(['seed','role'])
s = df[df['mode']=='synthetic'].set_index(['seed','role'])
for col in ['maxSpot','minSpot','maxCurve','minCurve','realizedAbs']:
    ratio = (b[col] / s[col]).describe()
    print(f'basket/synth {col}: min={ratio["min"]:.4f} max={ratio["max"]:.4f} mean={ratio["mean"]:.4f}')

# Padded seed
print()
print('Padded-seed rows (seed as 10-char):')
padded = df[df['seed'].astype(str).str.len()==10]
print(f'  count={len(padded)} out of {len(df)}')
print(f'  unique padded seeds: {sorted(padded["seed"].astype(str).unique())}')

# Concentration of outliers per seed
print()
print('Outlier positions per seed (columns where value flagged):')
# recompute IQR outliers per-mode
positions = {}
for mode in ['basket','spread','synthetic','x402']:
    sub = df[df['mode']==mode]
    for col in ['role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs','x402Total']:
        if sub[col].std() == 0: continue
        q1 = sub[col].quantile(0.25)
        q3 = sub[col].quantile(0.75)
        iqr = q3-q1
        lo = q1-1.5*iqr; hi = q3+1.5*iqr
        mask = (sub[col]<lo)|(sub[col]>hi)
        for _, row in sub[mask].iterrows():
            key = row['seed']
            positions.setdefault(key, []).append(f'{mode}.{col}')
# Filter out wallet_sum_pnl (float dust) and x402Total (bimodal)
cleaned = {k: [p for p in v if not p.endswith('.wallet_sum_pnl')] for k, v in positions.items()}
cleaned = {k: v for k, v in cleaned.items() if v}
for k in sorted(cleaned, key=lambda x: -len(cleaned[x])):
    print(f'  {k} ({len(cleaned[k])}): {cleaned[k][:6]}...' if len(cleaned[k])>6 else f'  {k} ({len(cleaned[k])}): {cleaned[k]}')

# x402 correlation settlementLegs x x402Total
x4 = df[df['mode']=='x402']
print()
print(f'x402 settlementLegs × x402Total correlation = {x4["settlementLegs"].corr(x4["x402Total"]):.3f}')
# Highest non-wallet within-mode pair
print()
print('Top within-mode correlation (excluding wallet_sum_pnl):')
for mode in ['basket','spread','synthetic','x402']:
    sub = df[df['mode']==mode].select_dtypes('number')
    cols = [c for c in sub.columns if c != 'wallet_sum_pnl' and sub[c].std() > 0]
    corr = sub[cols].corr().abs()
    # unstack
    pairs = []
    for i, c1 in enumerate(cols):
        for c2 in cols[i+1:]:
            pairs.append((c1, c2, corr.loc[c1,c2]))
    pairs.sort(key=lambda x: -x[2])
    top = pairs[0]
    print(f'  {mode}: {top[0]} × {top[1]} = {top[2]:.3f}')

# retail loss cluster in spread
print()
sub = df[df['mode']=='spread']
top5_losses = sub.nsmallest(5, 'role_pnl')[['seed','role','role_pnl']]
retail_count = (top5_losses['role']=='retail').sum()
print(f'Spread top-5 losses: retail count = {retail_count}/5')
print(top5_losses.to_string(index=False))

print()
print('Top-5 gains in spread:')
top5_gains = sub.nlargest(5, 'role_pnl')[['seed','role','role_pnl']]
print(top5_gains.to_string(index=False))
retail_gain = (top5_gains['role']=='retail').sum()
print(f'Retail count in top-5 gains: {retail_gain}/5')

# spread role means
print()
print('Spread role P&L stats:')
for role in ['retail','operator','analyst']:
    r = sub[sub['role']==role]['role_pnl']
    print(f'  {role}: n={len(r)} mean={r.mean():.2f} std={r.std():.2f}')

# x402Total extremes
print()
x4v = df[df['mode']=='x402']
print(f'x402Total: min={x4v["x402Total"].min():.2f} max={x4v["x402Total"].max():.2f} mean={x4v["x402Total"].mean():.2f} sum={x4v["x402Total"].sum():.2f} std={x4v["x402Total"].std():.2f}')
# anchor seeds
xmin_seeds = x4v[x4v['x402Total']==x4v['x402Total'].min()]['seed'].unique()
xmax_seeds = x4v[x4v['x402Total']==x4v['x402Total'].max()]['seed'].unique()
print(f'  LOW anchor seed(s): {xmin_seeds}')
print(f'  HIGH anchor seed(s): {xmax_seeds}')

# padded seed anchor role
print()
print('Padded-seed outlier contribution:')
padded_ids = set(padded['seed'].unique())
padded_pos_count = 0
total_pos_count = 0
for k, v in cleaned.items():
    total_pos_count += len(v)
    if k in padded_ids:
        padded_pos_count += len(v)
print(f'  padded seeds contribute {padded_pos_count} of {total_pos_count} outlier positions')
