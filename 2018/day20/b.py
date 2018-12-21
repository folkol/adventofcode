from collections import defaultdict, deque

with open('paths.dat') as f:
    pattern = f.read()


def parse_alternatives(i, rest):
    alernatives = []
    nesting = 0
    c = start = i + 1
    while c < len(rest):
        if rest[c] == '(':
            nesting += 1
        elif rest[c] == ')':
            if nesting == 0:
                alernatives.append((start, c))
                c += 1
                break
            else:
                nesting -= 1
        elif rest[c] == '|' and nesting == 0:
            alernatives.append((start, c))
            start = c + 1
        c += 1
    return c - i, alernatives


def paths(pos, start, end, pattern):
    if (pos, start, end, pattern) in seen:
        return
    seen.add((pos, start, end, pattern))
    i = start
    while i < end:
        c = pattern[i]
        if c == '(':
            chars, alternatives = parse_alternatives(i, pattern)
            for alternative in alternatives:
                cont_pos = paths(pos, *alternative, pattern)
                paths(cont_pos, i + chars, end, pattern)
            i += chars
            break
        else:
            if c == 'N':
                adj = pos[0], pos[1] - 1
            elif c == 'E':
                adj = pos[0] + 1, pos[1]
            elif c == 'S':
                adj = pos[0], pos[1] + 1
            elif c == 'W':
                adj = pos[0] - 1, pos[1]
            else:
                raise ValueError('Unexpected c:', c)
            doors[pos].add(adj)
            doors[adj].add(pos)
            pos = adj
        i += 1
    return pos


def bfs():
    start = 0, 0
    q = deque()
    q.append(start)
    distances = {start: 0}
    while q:
        cell = q.popleft()
        for adjacent in [c for c in doors[cell]]:
            if adjacent not in distances:
                q.append(adjacent)
                distances[adjacent] = distances[cell] + 1
    return distances


seen = set()
doors = defaultdict(set)
paths((0, 0), 1, len(pattern) - 1, pattern)
distances = bfs()

far_away_rooms = sum(1 for d in distances.values() if d >= 1000)
assert far_away_rooms == 8615, far_away_rooms
print(far_away_rooms)
