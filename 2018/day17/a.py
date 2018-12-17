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


def inside_bucket(droplet):
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


def cell_at(droplet):
    return scan.get(droplet, '.')


def cell_below(droplet):
    return scan.get((droplet[0], droplet[1] + 1), '.')


def cell_left(droplet):
    return scan.get((droplet[0] - 1, droplet[1]))


def cell_right(droplet):
    return scan.get((droplet[0] + 1, droplet[1]))


def out_of_play(droplet):
    return droplet[1] > y_max


def move_up(droplet):
    return droplet[0], droplet[1] - 1


def move_down(droplet):
    return droplet[0], droplet[1] + 1


def move_left(droplet):
    return droplet[0] - 1, droplet[1]


def move_right(droplet):
    return droplet[0] + 1, droplet[1]


def scan_down(droplet):
    while cell_below(droplet) in '.|':
        if out_of_play(droplet) or cell_at(droplet) == '|':
            return
        scan[droplet] = '|'
        droplet = move_down(droplet)
    while inside_bucket(droplet):
        fill_layer(droplet)
        droplet = move_up(droplet)
    scan_left(droplet)
    scan_right(droplet)


def fill_layer(droplet):
    for cell in inside_bucket(droplet):
        scan[cell] = '~'


def scan_left(droplet):
    while cell_below(droplet) in '#~':
        if cell_at(droplet) != '~':
            scan[droplet] = '|'
        if cell_left(droplet) == '#':
            break
        droplet = move_left(droplet)
    else:
        scan_down(droplet)


def scan_right(droplet):
    while cell_below(droplet) in '#~':
        if cell_at(droplet) != '~':
            scan[droplet] = '|'
        if cell_right(droplet) == '#':
            break
        droplet = move_right(droplet)
    else:
        scan_down(droplet)


scan_down(spring)

wet_cells = sum(cell in '~|' for (x, y), cell in scan.items() if y_min <= y <= y_max)
assert wet_cells == 33242, wet_cells
print(wet_cells)
