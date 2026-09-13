import hashlib
def fp(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]

# Prior fingerprints for actionlint at aeon.yml:286 = 7036da7e0e0ce1a3
print('my:', fp('actionlint/shellcheck|.github/workflows/aeon.yml|L286'))
print('no-prefix:', fp('actionlint/shellcheck|aeon.yml|L286'))
print('slug:', fp('actionlint|.github/workflows/aeon.yml|L286'))
print('with source:', fp('actionlint-shellcheck|.github/workflows/aeon.yml|L286'))
print('shellcheck only:', fp('shellcheck|.github/workflows/aeon.yml|L286'))
