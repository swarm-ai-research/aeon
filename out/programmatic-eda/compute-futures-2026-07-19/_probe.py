import pandas as pd, os
proofs = '/home/runner/work/aeon/aeon/memory/gitlawb-compute-futures-proofs'
recent = ['2026-07-13','2026-07-14','2026-07-15','2026-07-16','2026-07-17','2026-07-18','2026-07-19']

print('=== spread realizedAbs history ===')
for d in recent:
    p = f'{proofs}/{d}.csv'
    if not os.path.exists(p): continue
    df = pd.read_csv(p)
    sr = df[df['mode']=='spread']['realizedAbs']
    q1, q3 = sr.quantile(0.25), sr.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
    out = ((sr < lo) | (sr > hi)).sum()
    print(f'{d}  n={len(sr)} mean={sr.mean():.0f} std={sr.std():.0f} iqr_out={out} ({100*out/len(sr):.2f}%)')

print()
print('=== basket settlementLegs history ===')
for d in recent:
    p = f'{proofs}/{d}.csv'
    if not os.path.exists(p): continue
    df = pd.read_csv(p)
    sl = df[df['mode']=='basket']['settlementLegs']
    q1, q3 = sl.quantile(0.25), sl.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
    out = ((sl < lo) | (sl > hi)).sum()
    print(f'{d}  dist={dict(sl.value_counts().sort_index())} iqr_out={out} ({100*out/len(sl):.2f}%)')

print()
print('=== basket maxCurve history (the collapsing streak) ===')
for d in recent:
    p = f'{proofs}/{d}.csv'
    if not os.path.exists(p): continue
    df = pd.read_csv(p)
    mc = df[df['mode']=='basket']['maxCurve']
    q1, q3 = mc.quantile(0.25), mc.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
    out = ((mc < lo) | (mc > hi)).sum()
    print(f'{d}  min={mc.min():.4f} max={mc.max():.4f} mean={mc.mean():.4f} std={mc.std():.4f} iqr_out={out} ({100*out/len(mc):.2f}%)')

print()
print('=== spread settlementLegs history (was 25% yesterday) ===')
for d in recent:
    p = f'{proofs}/{d}.csv'
    if not os.path.exists(p): continue
    df = pd.read_csv(p)
    sl = df[df['mode']=='spread']['settlementLegs']
    q1, q3 = sl.quantile(0.25), sl.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
    out = ((sl < lo) | (sl > hi)).sum()
    print(f'{d}  dist={dict(sl.value_counts().sort_index())} iqr_out={out} ({100*out/len(sl):.2f}%)')

print()
print('=== curve tails today across modes ===')
today = pd.read_csv(f'{proofs}/2026-07-19.csv')
for m in ['basket','spread','synthetic','x402']:
    for col in ['minCurve','maxCurve']:
        c = today[today['mode']==m][col]
        q1, q3 = c.quantile(0.25), c.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
        out = ((c < lo) | (c > hi)).sum()
        print(f'{m:10s} {col:10s}  min={c.min():.4f} max={c.max():.4f} std={c.std():.4f} iqr_out={out} ({100*out/len(c):.2f}%)')

print()
print('=== x402Total history ===')
for d in recent:
    p = f'{proofs}/{d}.csv'
    if not os.path.exists(p): continue
    df = pd.read_csv(p)
    x = df[df['mode']=='x402']['x402Total']
    print(f'{d}  min={x.min():.2f} max={x.max():.2f} mean={x.mean():.2f} sum={x.sum():.2f}')

print()
print('=== x402 sub-threshold correlation churn tracking ===')
for d in recent:
    p = f'{proofs}/{d}.csv'
    if not os.path.exists(p): continue
    df = pd.read_csv(p)
    x = df[df['mode']=='x402']
    r_sl = x['settlementLegs'].corr(x['x402Total'])
    r_mc = x['maxCurve'].corr(x['x402Total'])
    r_seed = x['seed'].corr(x['x402Total'])
    print(f'{d}  settlementLegs×x402Total={r_sl:+.3f}  maxCurve×x402Total={r_mc:+.3f}  seed×x402Total={r_seed:+.3f}')

print()
print('=== spread wallet_sum_pnl σ drift (was drifting up) ===')
for d in recent:
    p = f'{proofs}/{d}.csv'
    if not os.path.exists(p): continue
    df = pd.read_csv(p)
    ws = df[df['mode']=='spread']['wallet_sum_pnl']
    print(f'{d}  mean={ws.mean():.3e} std={ws.std():.3e}')

# synth vs x402 role_pnl equivalence
print()
print('=== synth vs x402 role_pnl equivalence ===')
today_synth = today[today['mode']=='synthetic'][['seed','role','role_pnl']].sort_values(['seed','role']).reset_index(drop=True)
today_x402 = today[today['mode']=='x402'][['seed','role','role_pnl']].sort_values(['seed','role']).reset_index(drop=True)
diff = (today_synth['role_pnl'] - today_x402['role_pnl']).abs().max()
print(f'max |diff role_pnl| synth vs x402: {diff}')

# Row counts and seeds
print()
print('=== row/col shape ===')
print(f'today rows={len(today)} cols={len(today.columns)}')
prev = pd.read_csv(f'{proofs}/2026-07-18.csv')
print(f'yday  rows={len(prev)} cols={len(prev.columns)}')
print(f'today seeds unique={sorted(today["seed"].unique().tolist())}')
