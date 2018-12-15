from collections import deque, defaultdict

adjacents = [(0, -1), (0, 1), (-1, 0), (1, 0)]

with open('cave.dat') as f:
    mobs = {}
    map = {}
    for y, line in enumerate(f):
        for x, cell in enumerate(line.rstrip('\n')):
            if cell in 'EG':
                mobs[(x, y)] = cell
                cell = '.'
            map[(x, y)] = cell


def show():
    global y, x, cell
    for y in range(9):
        for x in range(9):
            cell = mobs.get((x, y)) or map.get((x, y), ' ')
            print(cell, end='')
        print()

hp = {pos: 200 for pos in mobs}
def reading_order(item):
    try:
        (x, y), cell = item
    except:
        (x, y) = item
    return y, x


while True:
    for (x, y), current in sorted(mobs.items(), key=reading_order):
        enemies = [pos for pos, mob in mobs.items() if mob != current]
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
            mobs[step] = current
            del mobs[(x, y)]
        adjacent_enemies = [foo in enemies for foo in [(x + dx, y + dy) for dx, dy in adjacents]]
        # target = sorted(adjacent_enemies, key=lambda e: (200 - hp[e], *reading_order(e)))[0]
        show()
