import pathlib
lines = pathlib.Path('.github/workflows/aeon.yml').read_text().splitlines()
for line in [85, 121, 133]:
    start = max(0, line-3); end = min(len(lines), line+3)
    print(f'--- line {line} ---')
    for i in range(start, end):
        marker = '>>>' if i+1 == line else '   '
        print(f'{marker} {i+1}: {lines[i]}')
