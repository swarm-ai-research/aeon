import hashlib, itertools

TARGET = '0255635a6c12c703'  # SC2129 aeon.yml L286
# Known: rule=actionlint/shellcheck/SC2129, file=.github/workflows/aeon.yml, step=SC2129:L286

# Try various combinations
rule_opts = [
    'actionlint/shellcheck/SC2129',
    'actionlint/shellcheck',
    'actionlint/SC2129',
    'shellcheck/SC2129',
    'SC2129',
    'actionlint',
]
file_opts = [
    '.github/workflows/aeon.yml',
    'aeon.yml',
    'workflows/aeon.yml',
]
step_opts = [
    'SC2129:L286',
    'SC2129:286',
    'L286',
    '286',
    'SC2129',
    'shellcheck',
    'SC2129 aeon.yml:286',
    '',
]
seps = ['|', ':', '/', '\n', ' ', '::']

for r, f, s, sep in itertools.product(rule_opts, file_opts, step_opts, seps):
    k = f'{r}{sep}{f}{sep}{s}'
    h = hashlib.sha256(k.encode()).hexdigest()[:16]
    if h == TARGET:
        print('MATCH:', repr(k))
# Also try 4-field (with line separately)
for r, f, s in itertools.product(rule_opts, file_opts, step_opts):
    for line in [0, 286, '286', 'L286']:
        for sep in ['|', ':']:
            k = f'{r}{sep}{f}{sep}{s}{sep}{line}'
            h = hashlib.sha256(k.encode()).hexdigest()[:16]
            if h == TARGET:
                print('MATCH4:', repr(k))
