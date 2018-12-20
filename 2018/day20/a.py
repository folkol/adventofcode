rest = r"^ENWWW(NEEE|SSE(EE|N))$"
rest = r"^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"


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


def paths(base, rest):
    if '(' in rest:
        start = rest.index('(')
        chars, alternatives = parse_alternatives(rest[start:])
        for alternative in alternatives:
            yield from paths(base + rest[:start], alternative + rest[start + chars + 1:])
    else:
        yield base + rest[:-1]


for path in paths('', rest[1:]):
    print(path)
