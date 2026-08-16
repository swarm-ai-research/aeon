import re
lines = open('.github/workflows/aeon.yml').read().splitlines()
target = 98
print(f'total lines: {len(lines)}')
print(f'line {target}: {lines[target-1]!r}')
for i in range(target-1, -1, -1):
    m = re.match(r'\s*-\s*name:\s*(.+?)\s*$', lines[i])
    if m:
        print(f'HIT at line {i+1}: {m.group(1)!r}')
        break
    if i > target - 20:
        pass
    else:
        break
else:
    print('no hit in first 20 lines back')
# Try with pathless open
import os
print('cwd:', os.getcwd())
print('exists aeon.yml:', os.path.exists('aeon.yml'))
print('exists .github/workflows/aeon.yml:', os.path.exists('.github/workflows/aeon.yml'))
