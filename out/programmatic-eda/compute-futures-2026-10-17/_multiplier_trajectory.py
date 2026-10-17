import pandas as pd
import glob, os

csvs = sorted(glob.glob('memory/gitlawb-compute-futures-proofs/*.csv'))
print(f'{"date":<12} {"mult_minSpot":>14} {"mult_maxSpot":>14}')
for p in csvs[-30:]:
    date = os.path.basename(p).replace('.csv','')
    try:
        d = pd.read_csv(p)
        b = d[d['mode']=='basket'].groupby('seed')['minSpot'].first()
        s = d[d['mode']=='synthetic'].groupby('seed')['minSpot'].first()
        r = (b/s).dropna()
        bm = d[d['mode']=='basket'].groupby('seed')['maxSpot'].first()
        sm = d[d['mode']=='synthetic'].groupby('seed')['maxSpot'].first()
        rm = (bm/sm).dropna()
        print(f'{date:<12} {r.mean():>14.6f} {rm.mean():>14.6f}  (uniq={len(r.round(6).unique())}/{len(rm.round(6).unique())})')
    except Exception as e:
        print(f'{date}  ERROR: {e}')
