from collections import defaultdict

pattern = r"^ENWWW(NEEE|SSE(EE|N))$"
pattern = r"^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"


def parse_alternatives(rest):
    alernatives = []
    nesting = 0
    start = 1
    c = 1
    while True:
        if rest[c] == '(':
            nesting += 1
        elif rest[c] == ')':
            if nesting == 0:
                alernatives.append(rest[start:c])
                break
            else:
                nesting -= 1
        elif rest[c] == '|' and nesting == 0:
            alernatives.append(rest[start:c])
            start = c + 1
        c += 1
    return c, alernatives


doors = defaultdict(set)


def paths(pos, pattern):
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == '(':
            chars, alternatives = parse_alternatives(pattern)
            for alternative in alternatives:
                paths(pos, alternative + pattern[i:])
            i += chars
        elif c == 'N':
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


for path in paths((0, 0), pattern[1:]):
    print(path)
