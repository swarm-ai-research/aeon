import hashlib
# Verify that spaces-not-underscores fingerprinting matches all the resolved entries
cases = [
    ('d42af71c10f40be0', 'zizmor/artipacked', '.github/workflows/aeon.yml', 'Early checkout'),
    ('0c66d5f673cf0c0e', 'zizmor/artipacked', '.github/workflows/aeon.yml', 'Checkout repo'),
    ('d2fc7a994dfa1fec', 'zizmor/artipacked', '.github/workflows/chain-runner.yml', 'Checkout repo'),
    ('024d092e2be757bb', 'zizmor/concurrency-limits', '.github/workflows/gitlawb-repo-bootstrap.yml', 'description: "Repo name to create on the GitLawb node"'),
    ('026cbff74a338284', 'zizmor/artipacked', '.github/workflows/messages.yml', 'Checkout repo'),
    ('e227de85a27cbd59', 'zizmor/artipacked', '.github/workflows/sync-aeon-public-results.yml', 'Checkout aeon'),
    ('7c001f1bd15a8a23', 'zizmor/artipacked', '.github/workflows/sync-upstream.yml', 'Checkout fork'),
    # actionlint
    ('0255635a6c12c703', 'actionlint/shellcheck/SC2129', '.github/workflows/aeon.yml', 'SC2129:L286'),
    ('2d9e1020fb37b600', 'actionlint/shellcheck/SC2129', '.github/workflows/aeon.yml', 'SC2129:L601'),
    ('7fbcfbf6f94d70ea', 'actionlint/shellcheck/SC2034', '.github/workflows/chain-runner.yml', 'SC2034:L42'),
    ('7635603ae7ab5a80', 'actionlint/shellcheck/SC2129', '.github/workflows/chain-runner.yml', 'SC2129:L42'),
    ('6d07f1a8d9b9cd1d', 'actionlint/shellcheck/SC2155', '.github/workflows/chain-runner.yml', 'SC2155:L42'),
    ('a7f35ffd56f9fd84', 'actionlint/shellcheck/SC2155', '.github/workflows/fleet-runner.yml', 'SC2155:L186'),
    ('7a317867bd2ec5a6', 'actionlint/shellcheck/SC2086', '.github/workflows/fleet-runner.yml', 'SC2086:L301'),
    ('442b08b6e74e546d', 'actionlint/shellcheck/SC2034', '.github/workflows/messages.yml', 'SC2034:L69'),
    ('acd63f72d218312a', 'actionlint/shellcheck/SC2129', '.github/workflows/messages.yml', 'SC2129:L669'),
    ('29b17c2e50dd336d', 'actionlint/shellcheck/SC2129', '.github/workflows/messages.yml', 'SC2129:L734'),
    ('909e21530c20cc7b', 'actionlint/shellcheck/SC2129', '.github/workflows/messages.yml', 'SC2129:L815'),
]
ok = 0
for want, rule, file, step in cases:
    k = f'{rule}|{file}|{step}'
    h = hashlib.sha256(k.encode()).hexdigest()[:16]
    status = 'OK ' if h == want else 'MISS'
    print(status, want, h, repr(k))
    if h == want: ok += 1
print(f'{ok}/{len(cases)} match')
