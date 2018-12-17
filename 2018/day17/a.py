import re

scan = {}
spring = 500, 0
with open('scan.dat') as f:
    for line in f:
        match = re.search(r'x=(\d+)\.\.(\d+)', line)
        if match:
            start, end = match.groups()
            xs = range(int(start), int(end) + 1)
        match = re.search(r'x=(\d+)[ ,$]', line)
        if match:
            xs = [int(match.group(1))]
        match = re.search(r'y=(\d+)\.\.(\d+)', line)
        if match:
            start, end = match.groups()
            ys = range(int(start), int(end) + 1)
        match = re.search(r'y=(\d+)[ ,$]', line)
        if match:
            ys = [int(match.group(1))]
        for y in ys:
            for x in xs:
                scan[(x, y)] = '#'

min_x = min(x for x, y in scan)
max_x = max(x for x, y in scan)
min_y = min(y for x, y in scan)
max_y = max(y for x, y in scan)


def plot():
    global y, x
    for y in range(0, 3):
        print(f'   ', end='')
        for x in range(min_x - 1, max_x + 2):
            print(format(x, '03d')[y], end='')
        print()
    for y in range(0, max_y + 2):
        print(f'{y:02d} ', end='')
        for x in range(min_x - 1, max_x + 2):
            if (x, y) == (500, 0):
                print('+', end='')
            else:
                print(scan.get((x, y)) or '.', end='')
        print()


plot()
