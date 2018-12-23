import re
from operator import itemgetter

PATTERN = r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)'


def in_range(b, reference):
    def manhattan(a, b):
        return sum(abs(j - i) for i, j in zip(a, b))

    return manhattan(b[0:3], reference[0:3]) <= reference[3]


with open('coordinates.dat') as f:
    bots = [[int(g) for g in re.match(PATTERN, line).groups()] for line in f]

prime_bot = max(bots, key=itemgetter(3))
print(sum(1 for b in bots if in_range(b, prime_bot)))
