from collections import defaultdict
from pprint import pprint

pattern = r"^N(W|(S|W))N$"
pattern = r"^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
pattern = r"^ENWWW(NEEE|SSE(EE|N))$"
with open('pattern.dat') as f:
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
                alernatives.append(rest[start:c])
                c += 1
                break
            else:
                nesting -= 1
        elif rest[c] == '|' and nesting == 0:
            alernatives.append(rest[start:c])
            start = c + 1
        c += 1
    return c - i, alernatives


doors = defaultdict(set)


def paths(pos, pattern):
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == '(':
            chars, alternatives = parse_alternatives(i, pattern)
            for alternative in alternatives:
                paths(pos, alternative + pattern[i + chars:])
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


paths((0, 0), pattern[1:-1])

pprint(doors)
