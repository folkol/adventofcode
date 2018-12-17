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
    while cell_below(droplet) in '#~':
        if cell_left(droplet) == '#':
            left_wall = droplet[0] - 1
            break
        droplet = move_left(droplet)
    droplet = droplet
    while cell_below(droplet) in '#~':
        if cell_right(droplet) == '#':
            right_wall = droplet[0] + 1
            break
        droplet = move_right(droplet)
    if left_wall and right_wall:
        return [(x, droplet[1]) for x in range(left_wall + 1, right_wall)]


def cell_at(droplet):
    return scan.get(droplet, '.')


def cell_below(droplet):
    return scan.get((droplet[0], droplet[1] + 1), '.')


def cell_left(droplet):
    return scan.get((droplet[0] - 1, droplet[1]), '.')


def cell_right(droplet):
    return scan.get((droplet[0] + 1, droplet[1]), '.')


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


def flow_down(droplet):
    while cell_below(droplet) in '.|':
        if out_of_play(droplet) or cell_at(droplet) == '|':
            return
        scan[droplet] = '|'
        droplet = move_down(droplet)
    while inside_bucket(droplet):
        fill_layer(droplet)
        droplet = move_up(droplet)
    flow_left(droplet)
    flow_right(droplet)


def fill_layer(droplet):
    for cell in inside_bucket(droplet):
        scan[cell] = '~'


def flow_left(droplet):
    while cell_below(droplet) in '#~':
        if cell_at(droplet) != '~':
            scan[droplet] = '|'
        if cell_left(droplet) == '#':
            break
        droplet = move_left(droplet)
    else:
        flow_down(droplet)


def flow_right(droplet):
    while cell_below(droplet) in '#~':
        if cell_at(droplet) != '~':
            scan[droplet] = '|'
        if cell_right(droplet) == '#':
            break
        droplet = move_right(droplet)
    else:
        flow_down(droplet)


flow_down(spring)

wet_cells = sum(cell in '~' for (x, y), cell in scan.items() if y_min <= y <= y_max)
assert wet_cells == 27256, wet_cells
print(wet_cells)
