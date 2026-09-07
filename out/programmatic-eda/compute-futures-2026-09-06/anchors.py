import pandas as pd
df = pd.read_csv('memory/gitlawb-compute-futures-proofs/2026-09-06.csv')

for m in ['basket','synthetic','x402']:
    print(m, 'realizedAbs by seed:')
    rr = df[df['mode']==m].groupby('seed')['realizedAbs'].first().sort_values()
    print(rr.to_string(float_format=lambda x: f'{x:.3f}'))
    print()

print('=== basket minSpot / maxCurve outliers seeds ===')
b = df[df['mode']=='basket'].groupby('seed').first()
print('minSpot sorted:')
print(b['minSpot'].sort_values().to_string(float_format=lambda x: f'{x:.6f}'))
print()
print('maxCurve sorted:')
print(b['maxCurve'].sort_values().to_string(float_format=lambda x: f'{x:.6f}'))
print()

print('=== spread realizedAbs top-3 (outlier cluster) ===')
sp = df[df['mode']=='spread'].groupby('seed').first()
print(sp['realizedAbs'].sort_values(ascending=False).head(4).to_string(float_format=lambda x: f'{x:.2f}'))
print()

print('=== seed 202609062 breakdown ===')
s = df[df['seed']==202609062]
print(s[['mode','role','role_pnl']].to_string(index=False))
print()

print('=== seed 202609067 breakdown ===')
s = df[df['seed']==202609067]
print(s[['mode','role','role_pnl']].to_string(index=False))
print()

print('=== all padded participation in top-losses/gains ===')
sp2 = df[df['mode']=='spread'].copy()
sp2['padded'] = sp2['seed'] > 999999999
print('Padded share of spread retail losses (n=12 retail):')
retail = sp2[sp2['role']=='retail']
print('padded seeds:', sorted(retail[retail['padded']]['seed'].tolist()))
print('padded losses:', retail[retail['padded']][['seed','role_pnl']].to_string(index=False))
