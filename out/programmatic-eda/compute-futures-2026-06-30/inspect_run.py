import pandas as pd
df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-06-30.csv')

for mode in sorted(df['mode'].unique()):
    m = df[df['mode']==mode]
    num = m.select_dtypes('number')
    num = num.loc[:, num.std() > 0]
    c = num.corr().stack().reset_index()
    c.columns = ['a','b','r']
    c = c[c['a'] < c['b']]
    top = c.reindex(c['r'].abs().sort_values(ascending=False).index).head(6)
    print(f'--- {mode} top absolute r ---')
    print(top.to_string(index=False))
    print()

print('=== spread maxSpot distribution ===')
sp = df[df['mode']=='spread']['maxSpot']
print(sp.describe())
print('unique count:', sp.nunique())
print('sorted values:', sorted(sp.round(4).unique().tolist()))

q1, q3 = sp.quantile(0.25), sp.quantile(0.75)
iqr = q3 - q1
lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
print(f'q1={q1:.4f} q3={q3:.4f} IQR={iqr:.4f} fence=[{lo:.4f},{hi:.4f}]')
out = sp[(sp < lo) | (sp > hi)]
print(f'IQR outliers: {len(out)}')
print(out.round(4).tolist())

prior = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-06-28.csv')
print('\n=== shape compare ===')
print(f'2026-06-28: rows={len(prior)}, modes={sorted(prior["mode"].unique())}, seeds={prior["seed"].nunique()}')
print(f'2026-06-30: rows={len(df)}, modes={sorted(df["mode"].unique())}, seeds={df["seed"].nunique()}')

print('\n=== x402Total x402 mode compare ===')
print('2026-06-28:', prior[prior["mode"]=="x402"]["x402Total"].describe()[['mean','std','min','max']].to_dict())
print('2026-06-30:', df[df["mode"]=="x402"]["x402Total"].describe()[['mean','std','min','max']].to_dict())

print('\n=== role_pnl std per mode compare ===')
for m in sorted(df["mode"].unique()):
    ps = prior[prior["mode"]==m]["role_pnl"].std()
    ns = df[df["mode"]==m]["role_pnl"].std()
    pm = prior[prior["mode"]==m]["role_pnl"].mean()
    nm = df[df["mode"]==m]["role_pnl"].mean()
    print(f'{m}: prior mean={pm:.2f} std={ps:.2f}  today mean={nm:.2f} std={ns:.2f}')

sy = df[df["mode"]=="synthetic"].sort_values(['seed','role']).reset_index(drop=True)
x4 = df[df["mode"]=="x402"].sort_values(['seed','role']).reset_index(drop=True)
cols = ['role_pnl','wallet_sum_pnl','realizedAbs','minSpot','maxSpot','minCurve','maxCurve','settlementLegs']
print('\n=== synthetic vs x402 max |diff| ===')
for c in cols:
    print(f'{c}: {(sy[c]-x4[c]).abs().max()}')
