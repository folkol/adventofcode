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


def done(full_turns):
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


def move(pos, current, targets):
    x, y = pos
    distances = bfs((x, y), (x, y))
    target_distances = [distances.get(target) for target in targets if target in distances]
    if not target_distances:
        return None
    min_distance = min(target_distances)
    closest_target = [target for target in targets if target in distances and distances[target] == min_distance]
    chosen_target = sorted(closest_target, key=reading_order)[0]
    distance_from_chosen = bfs(chosen_target, (x, y))
    steps = [(x, y) for x, y in adjacents(x, y) if cave.get((x, y)) == '.' and (x, y) not in mobs]
    step = sorted(steps, key=lambda x: (distance_from_chosen[x], *reading_order(x)))[0]
    mobs[step] = current
    del mobs[(x, y)]
    return step


def attack(pos, enemies):
    x, y = pos
    adjacent_enemies = [(foo, mobs[foo]) for foo in adjacents(x, y) if foo in enemies]
    if adjacent_enemies:
        target = sorted(adjacent_enemies, key=lambda e: (e[1][1], *reading_order(e)))[0]
        target[1][1] -= 3
        if target[1][1] < 1:
            del mobs[target[0]]


def play_game():
    for round in count(1):
        for (x, y), current in sorted(mobs.items(), key=reading_order):
            if is_dead(current):
                continue
            enemies = [pos for pos, mob in mobs.items() if mob[0] != current[0]]
            if not enemies:
                done(round - 1)
            targets = [adjacent for x, y in enemies for adjacent in adjacents(x, y) if cave.get(adjacent) == '.']
            if not targets:
                continue
            if not any(foo in enemies for foo in adjacents(x, y)):
                new_pos = move((x, y), current, targets)
                if new_pos is None:
                    continue
                x, y = new_pos

            attack((x, y), enemies)


play_game()
