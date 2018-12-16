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


def done(full_turns, mobs, dead_elves):
    hps = [hp for _, hp in mobs.values()]
    hp = sum(hps)
    # assert full_turns * hp == 190777, (full_turns, hp)
    # plot_cave()
    print(f'Combat over after {full_turns} full turns. {dead_elves} dead elves. Total hp was {hp} and outcome was {full_turns * hp}')


def adjacents(x, y):
    return [(x + dx, y + dy) for (dx, dy) in [(0, -1), (0, 1), (-1, 0), (1, 0)]]


def unoccupied(cell, mobs):
    return cave.get(cell) == '.' and cell not in mobs


def bfs(start, current, mobs):
    """Breadth-first scan of the empty + current cells, returns a map of distances to each cell."""

    q = deque()
    q.append(start)
    distances = {start: 0}
    while q:
        cell = q.popleft()
        for adjacent in [c for c in adjacents(*cell) if c == current or unoccupied(c, mobs)]:
            if adjacent not in distances:
                q.append(adjacent)
                distances[adjacent] = distances[cell] + 1
    return distances


def is_dead(mob):
    return mob[1] < 1


def move(pos, current, targets, mobs):
    distances = bfs(pos, pos, mobs)
    target_distances = [distances.get(target) for target in targets if target in distances]
    if not target_distances:
        return None
    min_distance = min(target_distances)
    closest_target = [target for target in targets if target in distances and distances[target] == min_distance]
    chosen_target = sorted(closest_target, key=reading_order)[0]
    distance_from_chosen = bfs(chosen_target, pos, mobs)
    steps = [step for step in adjacents(*pos) if unoccupied(step, mobs)]
    step = sorted(steps, key=lambda step: (distance_from_chosen[step], *reading_order(step)))[0]
    mobs[step] = current
    del mobs[pos]
    return step


def take_damage(target, damage):
    target[1] -= damage


def attack(pos, enemies, mobs, attack_power):
    adjacent_enemies = [(foo, mobs[foo]) for foo in adjacents(*pos) if foo in enemies]
    if adjacent_enemies:
        enemy_pos, enemy = sorted(adjacent_enemies, key=lambda e: (e[1][1], *reading_order(e)))[0]
        take_damage(enemy, attack_power)
        if is_dead(enemy):
            del mobs[enemy_pos]


def are_enemies(mob, current):
    return mob[0] != current[0]


def play_game(elf_power, mobs):
    num_elves = sum(1 for mob in mobs.values() if mob[0] == 'E')
    for round in count():
        for pos, current in sorted(mobs.items(), key=reading_order):
            if is_dead(current):
                continue
            enemies = [pos for pos, mob in mobs.items() if are_enemies(mob, current)]
            if not enemies:
                dead_elves = num_elves - sum(1 for mob in mobs.values() if mob[0] == 'E')
                done(round, mobs, dead_elves)
                return dead_elves
            targets = [adjacent for enemy in enemies for adjacent in adjacents(*enemy) if cave.get(adjacent) == '.']
            if not targets:
                continue
            if not any(pos in enemies for pos in adjacents(*pos)):
                pos = move(pos, current, targets, mobs)
                if pos is None:
                    continue

            attack(pos, enemies, mobs, elf_power if current[0] == 'E' else 3)


for power in count(3):
    if not play_game(power, {pos: [race, hp] for pos, (race, hp) in mobs.items()}):
        break
