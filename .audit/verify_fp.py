import hashlib

# Prior fingerprints for actionlint
targets = {
    'a4607c388772': ('actionlint/SC2086', '.github/workflows/fleet-runner.yml', 'Run fleet task runner'),
}

# Try many combos
step_variants = ['Run fleet task runner', 'Run_fleet_task_runner', 'fleet-task-runner',
                 'run fleet task runner', 'Run', 'shellcheck']
rule_variants = ['actionlint/SC2086', 'actionlint/shellcheck', 'SC2086', 'shellcheck',
                 'actionlint/SC2086 high', 'SC2086:info']
file_variants = ['.github/workflows/fleet-runner.yml', 'fleet-runner.yml']

for want, (r, f, s) in targets.items():
    print(f'=== target {want} ===')
    for rr in rule_variants:
        for ff in file_variants:
            for ss in step_variants:
                key = f'{rr}|{ff}|{ss}'
                got = hashlib.sha256(key.encode()).hexdigest()[:12]
                if got == want:
                    print(f'MATCH  {got}  key={key!r}')

# Try just with a specific line number
for want, (r, f, s) in targets.items():
    for ln in range(280, 320):
        for step_prefix in [f'line{ln}', f'line {ln}', f'line-{ln}', f'{ln}', f'sc2086_{ln}']:
            key = f'{r}|{f}|{step_prefix}'
            got = hashlib.sha256(key.encode()).hexdigest()[:12]
            if got == want:
                print(f'MATCH  {got}  key={key!r}')

# Try with different rule id
for want, (r, f, s) in targets.items():
    for rr in ['actionlint/SC2086', 'actionlint', 'actionlint/shellcheck/SC2086']:
        for ss in ['Run fleet task runner', 'Run_fleet_task_runner']:
            key = f'{rr}|{f}|{ss}'
            got = hashlib.sha256(key.encode()).hexdigest()[:12]
            print(f'{got}  key={key!r}')
