from collections import defaultdict
from pprint import pprint

with open('pattern.dat') as f:
    pattern = f.read()
pattern = r"^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
pattern = r"^N(W|(S|W))N$"
pattern = r"^ENWWW(NEEE|SSE(EE|N))$"


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


doors = defaultdict(set)


def paths(pos, start, end, pattern):
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


paths((0, 0), 1, len(pattern) - 1, pattern)


def plot(doors):
    x_min = min(x for x, y in doors)
    x_max = max(x for x, y in doors)
    y_min = min(y for x, y in doors)
    y_max = max(y for x, y in doors)
    print('#', end='')
    for x in range(x_min, x_max + 1):
        print('#', end='')
        print('#', end='')
    print()
    for y in range(y_min, y_max + 1):
        print('#', end='')
        for x in range(x_min, x_max + 1):
            print('.', end='')
            print('|' if (x + 1, y) in doors[(x, y)] else '#', end='')
        print()
        print('#', end='')
        for x in range(x_min, x_max + 1):
            print('-' if (x, y + 1) in doors[(x, y)] else '#', end='')
            print('#', end='')
        print()



plot(doors)