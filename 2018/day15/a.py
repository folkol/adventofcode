import sys
from collections import deque
from itertools import count

with open('cave.dat') as f:
    mobs = {}
    cave = {}
    for y, line in enumerate(f):
        for x, cell in enumerate(line.rstrip('\n')):
            if cell in 'EG':
                mobs[(x, y)] = [cell, 200]
                cell = '.'
            cave[(x, y)] = cell


def plot_cave():
    for y in range(max(y for _, y in cave) + 1):
        for x in range(max(x for x, _ in cave) + 1):
            cell = mobs.get((x, y))
            if cell:
                print(cell[0], end='')
            else:
                print(cave.get((x, y), ' '), end='')
        print()


def reading_order(item):
    try:
        (x, y), cell = item
    except TypeError:
        (x, y) = item
    return y, x


def done():
    full_turns = round - 1
    hps = [hp for _, hp in mobs.values()]
    hp = sum(hps)
    assert full_turns * hp == 190777, (full_turns, hp)
    plot_cave()
    print(f'Combat over after {full_turns} full turns. Total hp was {hp} and outcome was {full_turns * hp}')
    sys.exit(0)


def adjacents(x, y):
    return [(x + dx, y + dy) for (dx, dy) in [(0, -1), (0, 1), (-1, 0), (1, 0)]]


def unoccupied(cell):
    return cave.get(cell) == '.' and cell not in mobs


def bfs(start, current):
    """Breadth-first scan of the empty + current cells, returns a map of distances to each cell."""

    q = deque()
    q.append(start)
    distances = {start: 0}
    while q:
        cell = q.popleft()
        for adjacent in [c for c in adjacents(*cell) if c == current or unoccupied(c)]:
            if adjacent not in distances:
                q.append(adjacent)
                distances[adjacent] = distances[cell] + 1
    return distances


def is_dead(mob):
    return mob[1] < 1


for round in count(1):
    for (x, y), current in sorted(mobs.items(), key=reading_order):
        # print(f'{x}, {y}, {current}: ')
        if is_dead(current):
            continue
        enemies = [pos for pos, mob in mobs.items() if mob[0] != current[0]]
        if not enemies:
            done()
        targets = [(dx, dy) for x, y in enemies for (dx, dy) in adjacents(x, y) if cave.get((dx, dy)) == '.']
        if not targets:
            continue
        if not any(foo in enemies for foo in adjacents(x, y)):
            visited = bfs((x, y), (x, y))
            in_visited = [visited.get(target) for target in targets if target in visited]
            if not in_visited:
                continue
            distance = min(in_visited)
            nearest = [target for target in targets if target in visited and visited[target] == distance]
            chosen = sorted(nearest, key=reading_order)[0]
            visited = bfs(chosen, (x, y))
            steps = [(x, y) for x, y in adjacents(x, y) if cave.get((x, y)) == '.' and (x, y) not in mobs]
            step = sorted(steps, key=lambda x: (visited[x], *reading_order(x)))[0]
            # print(f'{round}: {(x, y)} -> {step}')
            mobs[step] = current
            del mobs[(x, y)]
            (x, y) = step
        adjacent_enemies = [(foo, mobs[foo]) for foo in adjacents(x, y) if foo in enemies]
        if adjacent_enemies:
            target = sorted(adjacent_enemies, key=lambda e: (e[1][1], *reading_order(e)))[0]
            target[1][1] -= 3
            # print(f'{round}: ({x}, {y}) attacks {target}')
            if target[1][1] < 1:
                # print(f'{round}: {target} dies')
                del mobs[target[0]]
