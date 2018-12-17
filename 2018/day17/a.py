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

x_min = min(x for x, y in scan)
x_max = max(x for x, y in scan)
y_min = min(y for x, y in scan)
y_max = max(y for x, y in scan)


def inside(droplet):
    left_wall = right_wall = None
    scanner = droplet
    while scan.get((scanner[0], scanner[1] + 1), '.') in '#~':
        if scan.get((scanner[0] - 1, scanner[1])) == '#':
            left_wall = scanner[0] - 1
            break
        scanner = scanner[0] - 1, scanner[1]
    scanner = droplet
    while scan.get((scanner[0], scanner[1] + 1), '.') in '#~':
        if scan.get((scanner[0] + 1, scanner[1])) == '#':
            right_wall = scanner[0] + 1
            break
        scanner = scanner[0] + 1, scanner[1]
    if left_wall and right_wall:
        return [(x, droplet[1]) for x in range(left_wall + 1, right_wall)]


def left_fall(droplet):
    scanner = droplet
    while scan.get((scanner[0], scanner[1] + 1)):
        scanner = scanner[0] - 1, scanner[1]
    return scanner[0], scanner[1] + 1


def right_fall(droplet):
    scanner = droplet
    while scan.get((scanner[0], scanner[1] + 1)):
        scanner = scanner[0] + 1, scanner[1]
    return scanner[0], scanner[1] + 1


def fill(spring):
    droplet = spring
    while scan.get((droplet[0], droplet[1] + 1), '.') in '.|':  # scan down
        if droplet[1] > y_max or scan.get(droplet, '.') == '|':
            return
        scan[droplet] = '|'
        droplet = (droplet[0], droplet[1] + 1)
    while inside(droplet):
        for cell in inside(droplet):
            scan[cell] = '~'
        droplet = droplet[0], droplet[1] - 1
    scanner = droplet
    while scan.get((scanner[0], scanner[1] + 1), '.') in '#~':  # scan left
        if scan.get(scanner) != '~':
            scan[scanner] = '|'
        if scan.get((scanner[0] - 1, scanner[1])) == '#':  # left wall
            break
        scanner = (scanner[0] - 1, scanner[1])
    else:
        fill(scanner)
    scanner = droplet
    while scan.get((scanner[0], scanner[1] + 1), '.') in '#~':  # scan right
        if scan.get(scanner) != '~':
            scan[scanner] = '|'
        if scan.get((scanner[0] + 1, scanner[1])) == '#':  # right wall
            break
        scanner = (scanner[0] + 1, scanner[1])
    else:
        fill(scanner)


fill(spring)

watered_tiles = sum(cell in '~|' for (x, y), cell in scan.items() if y_min <= y <= y_max)
assert watered_tiles == 33242, watered_tiles
print(watered_tiles)
