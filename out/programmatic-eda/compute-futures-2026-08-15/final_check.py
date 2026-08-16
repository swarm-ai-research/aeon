import pandas as pd
df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-08-15.csv')
spread = df[df['mode']=='spread']
print('spread analyst mean:', round(spread[spread.role=='analyst']['role_pnl'].mean(),2))
print('spread operator mean:', round(spread[spread.role=='operator']['role_pnl'].mean(),2))
print('spread retail mean:', round(spread[spread.role=='retail']['role_pnl'].mean(),2))
print()
oc = pd.read_csv('out/programmatic-eda/compute-futures-2026-08-15/outlier_detector.csv')
mask = (oc['column'] != 'seed') & (oc['outlier_pct'] >= 10)
print('Cross-mode >=10 outlier rows (excluding seed):')
print(oc[mask].to_string(index=False))
# Deep look at maxSpot/minCurve outliers already excluded by design: basket/synth/x402 all show 25% because 3 of 12 seed groups are extremes
# These are structural, not new signals.

# Top within-mode correlations (excluding wallet_sum_pnl float dust and same-column pairs)
cm = pd.read_csv('out/programmatic-eda/compute-futures-2026-08-15/correlation_explorer.csv')
print()
print('=== top within-mode corr pairs (|r| >= 0.5, excluding wallet_sum_pnl) ===')
for _, row in cm.iterrows():
    pass  # csv format check
print(cm.head(2))
print('columns:', list(cm.columns))
