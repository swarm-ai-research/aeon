import pandas as pd, numpy as np
from collections import Counter

df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-08-19.csv')

print("=== SPREAD per-role ===")
sp = df[df['mode']=='spread']
for r in sorted(sp['role'].unique()):
    s = sp[sp['role']==r]['role_pnl']
    print(f"  {r}: n={len(s)} mean={s.mean():.2f} std={s.std():.2f} min={s.min():.2f} max={s.max():.2f}")

print("\n=== SPREAD top-5 losses ===")
for _, row in sp.nsmallest(5, 'role_pnl')[['seed','role','role_pnl']].iterrows():
    print(f"  seed={row['seed']} role={row['role']} pnl={row['role_pnl']:.2f}")

print("\n=== SPREAD top-5 gains ===")
for _, row in sp.nlargest(5, 'role_pnl')[['seed','role','role_pnl']].iterrows():
    print(f"  seed={row['seed']} role={row['role']} pnl={row['role_pnl']:.2f}")

print("\n=== BASKET per-role ===")
bk = df[df['mode']=='basket']
for r in sorted(bk['role'].unique()):
    s = bk[bk['role']==r]['role_pnl']
    print(f"  {r}: n={len(s)} mean={s.mean():.4f} std={s.std():.4f} min={s.min():.4f} max={s.max():.4f}")

print("\n=== SYNTH per-role ===")
sy = df[df['mode']=='synthetic']
for r in sorted(sy['role'].unique()):
    s = sy[sy['role']==r]['role_pnl']
    print(f"  {r}: n={len(s)} mean={s.mean():.4f} std={s.std():.4f} min={s.min():.4f} max={s.max():.4f}")

print("\n=== BASKET/SYNTH multiplier check ===")
for col in ['minSpot','maxSpot','minCurve','maxCurve','realizedAbs']:
    b_mean = df[df['mode']=='basket'][col].mean()
    s_mean = df[df['mode']=='synthetic'][col].mean()
    ratio = b_mean / s_mean if s_mean else float('nan')
    per_seed_ratios = []
    for seed in df['seed'].unique():
        b_val = df[(df['mode']=='basket') & (df['seed']==seed)][col].iloc[0]
        s_val = df[(df['mode']=='synthetic') & (df['seed']==seed)][col].iloc[0]
        if s_val:
            per_seed_ratios.append(b_val / s_val)
    per_seed_ratios = np.array(per_seed_ratios)
    print(f"  {col}: mean_ratio={ratio:.6f}  per_seed_min={per_seed_ratios.min():.6f} max={per_seed_ratios.max():.6f} std={per_seed_ratios.std():.2e}")

print("\n=== SYNTH == X402 role-level check ===")
for col in ['role_pnl','minSpot','maxSpot','minCurve','maxCurve','realizedAbs']:
    s = df[df['mode']=='synthetic'].sort_values(['seed','role']).reset_index(drop=True)[col]
    x = df[df['mode']=='x402'].sort_values(['seed','role']).reset_index(drop=True)[col]
    print(f"  {col}: identical={bool((s == x).all())}")

print("\n=== X402Total stats ===")
xt = df[df['mode']=='x402']['x402Total']
print(f"  n={len(xt)} min={xt.min():.4f} max={xt.max():.4f} mean={xt.mean():.4f} std={xt.std():.4f} range={xt.max()-xt.min():.4f}")

low_seed = df[(df['mode']=='x402') & (df['x402Total']==xt.min())]['seed'].tolist()
high_seed = df[(df['mode']=='x402') & (df['x402Total']==xt.max())]['seed'].tolist()
print(f"  LOW seed(s): {low_seed}")
print(f"  HIGH seed(s): {high_seed}")

print("\n=== Wallet_sum_pnl per mode ===")
for m in sorted(df['mode'].unique()):
    s = df[df['mode']==m]['wallet_sum_pnl']
    print(f"  {m}: mean={s.mean():.3e} std={s.std():.3e} maxabs={s.abs().max():.3e}")

print("\n=== Constants check ===")
for col in ['rounds','deniedWorkers']:
    print(f"  {col}: unique={df[col].unique().tolist()}")
print(f"  x402Total zero outside x402: max|value|={df[df['mode']!='x402']['x402Total'].abs().max():.3e}")

print("\n=== Outlier anchor breakdown (non-dust) ===")
key_cols_by_mode = {
    'basket': ['minCurve','maxCurve'],
    'spread': ['maxSpot','role_pnl'],
    'synthetic': ['maxCurve','minCurve','settlementLegs'],
    'x402': ['maxCurve','minCurve','settlementLegs'],
}
seed_anchor_counter = Counter()
for m, cols in key_cols_by_mode.items():
    dfm = df[df['mode']==m]
    for col in cols:
        q1 = dfm[col].quantile(0.25)
        q3 = dfm[col].quantile(0.75)
        iqr = q3 - q1
        lo = q1 - 1.5*iqr
        hi = q3 + 1.5*iqr
        outliers = dfm[(dfm[col] < lo) | (dfm[col] > hi)][['seed','role',col]]
        if len(outliers):
            for _, row in outliers.iterrows():
                seed_anchor_counter[int(row['seed'])] += 1
            print(f"  [{m}/{col}] outliers ({len(outliers)}): seeds={sorted(outliers['seed'].unique().tolist())}")

print(f"\n  Seed anchor totals (non-dust): {seed_anchor_counter.most_common()}")

print("\n=== Padded seed contribution ===")
padded_seeds = df[df['seed'] > 999999999]['seed'].unique()
print(f"  Padded seeds (>9 chars): {sorted(padded_seeds.tolist())}")
padded_rows = df[df['seed'] > 999999999]
print(f"  Padded rows: {len(padded_rows)}/{len(df)} = {100*len(padded_rows)/len(df):.1f}%")
padded_anchors = sum(v for k, v in seed_anchor_counter.items() if k > 999999999)
total_anchors = sum(seed_anchor_counter.values())
pct = 100*padded_anchors/total_anchors if total_anchors else 0
print(f"  Padded outlier anchors: {padded_anchors}/{total_anchors} = {pct:.1f}%")

print("\n=== Key correlations by mode (highest non-trivial) ===")
for m in sorted(df['mode'].unique()):
    dfm = df[df['mode']==m]
    numcols = [c for c in dfm.select_dtypes(include='number').columns if dfm[c].std() > 0]
    corrs = dfm[numcols].corr()
    print(f"\n  --- {m} ---")
    seen = set()
    pairs = []
    for i in range(len(corrs.columns)):
        for j in range(i+1, len(corrs.columns)):
            c1, c2 = corrs.columns[i], corrs.columns[j]
            r = corrs.iloc[i,j]
            if pd.notna(r):
                pairs.append((abs(r), c1, c2, r))
    pairs.sort(reverse=True)
    for ar, c1, c2, r in pairs[:7]:
        print(f"    {c1} x {c2}: r={r:+.4f}")

print("\n=== x402 settlementLegs x x402Total series check ===")
x4 = df[df['mode']=='x402']
r_sl_xt = x4[['settlementLegs','x402Total']].corr().iloc[0,1]
r_ra_xt = x4[['realizedAbs','x402Total']].corr().iloc[0,1]
print(f"  settlementLegs x x402Total = {r_sl_xt:+.4f}")
print(f"  realizedAbs x x402Total = {r_ra_xt:+.4f}")
