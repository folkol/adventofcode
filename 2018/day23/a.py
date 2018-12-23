import re
from operator import itemgetter


def in_range(b, reference):
    def manhattan(a, b):
        return sum(abs(j - i) for i, j in zip(a, b))

    return manhattan(b[0:3], reference[0:3]) <= reference[3]


bots = []

with open('coordinates.dat') as f:
    for line in f:
        match = re.match(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)', line)
        if match:
            x, y, z, r = [int(g) for g in match.groups()]
            bots.append((x, y, z, r))
prime_bot = max(bots, key=itemgetter(3))
print(prime_bot)
print(sum(1 for b in bots if in_range(b, prime_bot)))
