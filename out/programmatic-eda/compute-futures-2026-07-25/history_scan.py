import re, os

dates = ['2026-06-28','2026-07-03','2026-07-05','2026-07-07','2026-07-08','2026-07-09','2026-07-10','2026-07-12','2026-07-16','2026-07-17','2026-07-18','2026-07-20','2026-07-21','2026-07-24']

patterns = {
    'spread maxSpot': r'spread[^\n]*maxSpot[^\n]*?(\d+\.\d\d)%',
    'basket settlementLegs': r'basket[^\n]*settlementLegs[^\n]*?(\d+\.\d\d)%',
    'basket realizedAbs': r'basket[^\n]*realizedAbs[^\n]*?(\d+\.\d\d)%',
    'spread minSpot': r'spread[^\n]*minSpot[^\n]*?(\d+\.\d\d)%',
    'basket maxSpot': r'basket[^\n]*maxSpot[^\n]*?(\d+\.\d\d)%',
    'synth maxSpot': r'(?:synth|synthetic|x402)[^\n]*maxSpot[^\n]*?(\d+\.\d\d)%',
    'x402 settlementLegs x x402Total corr': r'settlementLegs.{0,3}(?:x|×).{0,3}x402Total[^\n]*?([+\-−]?\d+\.\d{3})',
}

for d in dates:
    p = f'memory/topics/compute-futures-eda/{d}.md'
    if not os.path.exists(p): continue
    with open(p) as fh:
        t = fh.read()
    row = [d]
    for lbl, pat in patterns.items():
        m = re.findall(pat, t)
        row.append(f'{lbl}={m[:3] if m else "-"}')
    print(' | '.join(row))
