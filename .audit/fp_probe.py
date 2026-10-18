import hashlib
TARGET = 'd42af71c10f40be0'
# Vary over step encodings, file forms, rule prefix presence, separator shape, with/without line
rules = ['zizmor/artipacked', 'artipacked']
files = ['.github/workflows/aeon.yml', 'aeon.yml', 'workflows/aeon.yml']
steps = ['Early checkout', 'Early_checkout', 'Early-checkout', 'early_checkout',
         'L83', '83', 'Early checkout:83', 'Early_checkout:83']
seps = ['|', ':', '/', '-', '\n']

found = []
for r in rules:
    for f in files:
        for s in steps:
            for sep in seps:
                k = f'{r}{sep}{f}{sep}{s}'
                h = hashlib.sha256(k.encode()).hexdigest()[:16]
                if h == TARGET:
                    found.append((k, h))
for pair in found:
    print(pair)
if not found:
    print('no match in sweep')
# Try alternative: rule|file|step then (line maybe included separately)
for r in rules:
    for f in files:
        for s in steps:
            for line in [0, 83, '83']:
                for sep in ['|', ':']:
                    k = f'{r}{sep}{f}{sep}{s}{sep}{line}'
                    h = hashlib.sha256(k.encode()).hexdigest()[:16]
                    if h == TARGET:
                        print('MATCH:', k)
