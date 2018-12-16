import sys
from collections import deque, defaultdict
from itertools import count

adjacents = [(0, -1), (0, 1), (-1, 0), (1, 0)]

with open('cave.dat') as f:
    mobs = {}
    map = {}
    for y, line in enumerate(f):
        for x, cell in enumerate(line.rstrip('\n')):
            if cell in 'EG':
                mobs[(x, y)] = [cell, 200, 3]
                cell = '.'
            map[(x, y)] = cell


def show():
    global y, x, cell
    for y in range(9):
        for x in range(9):
            cell = mobs.get((x, y))
            if cell:
                print(cell[0], end='')
            else:
                print(map.get((x, y), ' '), end='')
        print()
    print(*mobs.values())


def reading_order(item):
    try:
        (x, y), cell = item
    except:
        (x, y) = item
    return y, x


def play_game(power, mobs):
    for mob in mobs.values():
        if mob[0] == 'E':
            mob[2] = power
    dead_elves = 0
    for round in count(1):
        for (x, y), current in sorted(mobs.items(), key=reading_order):
            # print(f'{x}, {y}, {current}: ')
            if current[1] < 1:
                continue
            enemies = [pos
                       for pos, mob in mobs.items()
                       if mob[0] != current[0]]
            if not enemies:
                full_turns = round - 1
                hps = [hp for _, hp, _ in mobs.values()]
                hp = sum(hps)
                print(f'Combat over after {full_turns} full turns. {dead_elves} dead elves with {power} attack power. Total hp was {hp} and outcome was {full_turns * hp}')
                # show()
                return dead_elves
            targets = [(x + dx, y + dy)
                       for x, y in enemies
                       for (dx, dy) in adjacents
                       if map.get((x + dx, y + dy)) == '.']
            if not targets:
                continue
            if not any(foo in enemies for foo in [(x + dx, y + dy) for dx, dy in adjacents]):
                q = deque()
                q.append((x, y))
                visited = {(x, y): 1}
                parents = defaultdict(list)
                while q:
                    node = q.popleft()
                    for adjacent in [(node[0] + dx, node[1] + dy)
                                     for (dx, dy) in adjacents
                                     if map.get((node[0] + dx, node[1] + dy)) == '.'
                                        and (node[0] + dx, node[1] + dy) not in mobs]:
                        if adjacent not in visited:
                            q.append(adjacent)
                            visited[adjacent] = visited[node] + 1
                            parents[adjacent].append(node)
                        elif visited[node] == visited[adjacent]:
                            parents[adjacent].append(node)
                in_visited = [visited.get(target) for target in targets if target in visited]
                if not in_visited:
                    continue
                distance = min(in_visited)
                nearest = [target for target in targets if target in visited and visited[target] == distance]
                chosen = sorted(nearest, key=reading_order)[0]
                q = deque()
                q.append(chosen)
                visited = {chosen: 0}
                while q:
                    node = q.popleft()
                    for adjacent in [(node[0] + dx, node[1] + dy)
                                     for (dx, dy) in adjacents
                                     if (node[0] + dx, node[1] + dy) == (x, y) or
                                        (map.get((node[0] + dx, node[1] + dy)) == '.'
                                         and (node[0] + dx, node[1] + dy) not in mobs)]:
                        if adjacent not in visited:
                            q.append(adjacent)
                            visited[adjacent] = visited[node] + 1
                steps = [(x + dx, y + dy) for (dx, dy) in adjacents if
                         map.get((x + dx, y + dy)) == '.' and (x + dx, y + dy) not in mobs]
                step = sorted(steps, key=lambda x: (visited[x], *reading_order(x)))[0]
                # print(f'{round}: {(x, y)} -> {step}')
                mobs[step] = current
                del mobs[(x, y)]
                (x, y) = step
            adjacent_enemies = [(foo, mobs[foo]) for foo in [(x + dx, y + dy) for dx, dy in adjacents] if
                                foo in enemies]
            if adjacent_enemies:
                target = sorted(adjacent_enemies, key=lambda e: (e[1][1], *reading_order(e)))[0]
                target[1][1] -= current[2]
                # print(f'{round}: ({x}, {y}) attacks {target}')
                if target[1][1] < 1:
                    # print(f'{round}: {target} dies')
                    del mobs[target[0]]
                    if target[1][0] == 'E':
                        dead_elves += 1


for power in count(3):
    if not play_game(power, {pos: [race, hp, power] for pos, (race, hp, power) in mobs.items()}):
        break
