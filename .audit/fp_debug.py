import hashlib

# Try different step values to find what produced ca298be1d2d1
target = 'ca298be1d2d1'
rule = 'zizmor/undocumented-permissions'
f = '.github/workflows/aeon.yml'

for step_try in ['(unknown)', 'top', '', 'Run', 'run', 'Aeon', 'aeon',
                 'unknown', 'null', 'None', 'anonymous']:
    h = hashlib.sha256(f"{rule}|{f}|{step_try}".encode()).hexdigest()[:12]
    hit = '<<' if h == target else ''
    print(f"{h}  step={step_try!r} {hit}")
