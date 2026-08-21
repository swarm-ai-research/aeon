import pandas as pd, numpy as np
df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-08-21.csv')

print("=== Per-mode conservation ===")
for m, g in df.groupby('mode'):
    print(f"{m:10s}: mean={g['wallet_sum_pnl'].mean():+.3e} std={g['wallet_sum_pnl'].std():.3e} min={g['wallet_sum_pnl'].min():+.3e} max={g['wallet_sum_pnl'].max():+.3e}")

print("\n=== Spread role_pnl by role ===")
sp = df[df['mode']=='spread']
for r, g in sp.groupby('role'):
    print(f"  {r:9s} n={len(g):2d} mean={g['role_pnl'].mean():+.2f} std={g['role_pnl'].std():.2f} min={g['role_pnl'].min():+.2f} max={g['role_pnl'].max():+.2f}")

print("\n=== Spread top-5 losses ===")
print(sp.nsmallest(5, 'role_pnl')[['seed','role','role_pnl']].to_string(index=False))
print("\n=== Spread top-5 gains ===")
print(sp.nlargest(5, 'role_pnl')[['seed','role','role_pnl']].to_string(index=False))

print("\n=== basket/synthetic price multiplier per-seed ===")
b = df[df['mode']=='basket'].groupby('seed').first().reset_index()
s = df[df['mode']=='synthetic'].groupby('seed').first().reset_index()
merged = b.merge(s, on='seed', suffixes=('_b','_s'))
for col in ['minSpot','maxSpot','minCurve','maxCurve','realizedAbs']:
    ratio = merged[f'{col}_b'] / merged[f'{col}_s']
    print(f"  {col:12s} mean={ratio.mean():.6f} std={ratio.std():.6e} min={ratio.min():.6f} max={ratio.max():.6f}")

print("\n=== synth vs x402 role-level identity ===")
sy = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)
x4 = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)
for col in ['role_pnl','wallet_sum_pnl','minSpot','maxSpot','minCurve','maxCurve','realizedAbs']:
    diff = (sy[col] - x4[col]).abs().max()
    print(f"  {col:15s} max_abs_diff = {diff:.3e}")
x402 = df[df['mode']=='x402']
print(f"  x402Total mean={x402['x402Total'].mean():.3f} min={x402['x402Total'].min():.3f} max={x402['x402Total'].max():.3f} std={x402['x402Total'].std():.3f}")

print("\n=== x402 correlations ===")
x = df[df['mode']=='x402']
print(f"  settlementLegs x x402Total: {x['settlementLegs'].corr(x['x402Total']):+.4f}")
print(f"  realizedAbs x x402Total: {x['realizedAbs'].corr(x['x402Total']):+.4f}")

print("\n=== Padded seed rows ===")
df['seed_str'] = df['seed'].astype(str)
df['padded'] = df['seed_str'].str.len() == 10
print(f"  padded rows: {df['padded'].sum()}/{len(df)} ({df['padded'].mean()*100:.1f}%)")
print(f"  padded seeds: {sorted(df[df['padded']]['seed'].unique())}")

print("\n=== Super-anchor: outlier positions per seed (non-dust) ===")
seed_positions = {s: 0 for s in df['seed'].unique()}
seed_detail = {s: [] for s in df['seed'].unique()}
numeric = ['role_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs','x402Total']
for m in df['mode'].unique():
    dm = df[df['mode']==m]
    for col in numeric:
        vals = dm[col]
        if vals.std() < 1e-9:
            continue
        q1, q3 = vals.quantile(0.25), vals.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
        outliers = dm[(vals < lo) | (vals > hi)]
        for _, row in outliers.iterrows():
            seed_positions[row['seed']] += 1
            seed_detail[row['seed']].append((m, col, row['role'], 'LOW' if row[col]<lo else 'HIGH', row[col]))

for s in sorted(seed_positions, key=lambda k: -seed_positions[k]):
    if seed_positions[s] > 0:
        print(f"  seed {s}: {seed_positions[s]} positions")
        for d in seed_detail[s][:10]:
            print(f"    - {d[0]}/{d[1]}/{d[2]} {d[3]} {d[4]:.4f}")

total = sum(seed_positions.values())
padded_pos = sum(v for k,v in seed_positions.items() if len(str(k))==10)
print(f"\n  TOTAL non-dust outlier positions: {total}")
print(f"  Padded contribution: {padded_pos}/{total} ({padded_pos/total*100:.1f}%)" if total else "  none")

# Cross-mode outlier pcts (relevant for finding tiers)
print("\n=== Per-mode outlier_pct >= 10% (excl seed) ===")
for m in df['mode'].unique():
    dm = df[df['mode']==m]
    for col in numeric:
        vals = dm[col]
        if vals.std() < 1e-9:
            continue
        q1, q3 = vals.quantile(0.25), vals.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
        n_out = ((vals < lo) | (vals > hi)).sum()
        pct = n_out / len(vals) * 100
        if pct >= 10:
            print(f"  {m:10s} {col:15s} {n_out}/{len(vals)} = {pct:.2f}%")
