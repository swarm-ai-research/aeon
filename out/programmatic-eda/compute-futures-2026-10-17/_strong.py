import pandas as pd
df = pd.read_csv('out/programmatic-eda/compute-futures-2026-10-17/correlations_by_mode.csv')
df.rename(columns={'Unnamed: 0':'col'}, inplace=True)
cols = [c for c in df.columns if c not in ('col','mode')]
print('Strong pairs (|r| >= 0.8) per mode:')
for m, grp in df.groupby('mode'):
    g = grp.set_index('col')[cols]
    seen = set()
    for a in g.index:
        for b in g.columns:
            if a == b: continue
            if (b,a) in seen: continue
            r = g.loc[a, b]
            if pd.notna(r) and abs(r) >= 0.8:
                seen.add((a,b))
                print('  ' + m + ': ' + a + ' ~ ' + b + ': r=' + '%.3f' % r)
