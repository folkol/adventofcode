from math import inf

steps = open('path.dat').read().split(",")

DELTAS = {
    'nw': (-1, 1, 0),
    'n': (0, 1, -1),
    'ne': (1, 0, -1),
    'se': (1, -1, 0),
    's': (0, -1, 1),
    'sw': (-1, 0, 1)
}


def distance(*xs):
    return max(*map(abs, xs))


max_distance = -inf
x, y, z = 0, 0, 0
for step in steps:
    dx, dy, dz = DELTAS[step]
    x, y, z = x + dx, y + dy, z + dz
    max_distance = max(max_distance, distance(x, y, z))

print(max_distance)
