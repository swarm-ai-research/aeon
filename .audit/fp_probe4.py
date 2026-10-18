import hashlib
# Discover which line the prior fingerprint used
for n in range(1, 200):
    k = f'zizmor/artipacked|.github/workflows/aeon.yml|L{n}'
    h = hashlib.sha256(k.encode()).hexdigest()[:16]
    if h == 'd42af71c10f40be0':
        print('MATCH line', n, k)
