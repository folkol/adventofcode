from collections import Counter
from itertools import count

import matplotlib.pyplot as plt
import numpy as np


def distance(x1, y1):
    """Returns a function that calculates the manhattan distance from x1, y1."""

    def inner(coordinate):
        x2, y2 = coordinate
        return abs(x2 - x1) + abs(y2 - y1)

    return inner


def show(winner):
    """Plots the voronoi cells and their seeds."""

    def color(label, cap=75):
        return ((int(label.upper(), 16) * 17) % cap,
                (int(label.upper(), 16) * 17 * 17) % cap,
                (int(label.upper(), 16) * 17 * 17 * 17) % cap)

    fig, ax = plt.subplots()
    data = np.zeros((right + margin, bottom + margin, 3)).astype(np.uint8)
    for x in range(right + margin):
        for y in range(bottom + margin):
            l = label.get((x, y))
            if l:
                data[x, y] = color(l)
            if winner and label.get((x, y)) == label.get(winner).lower():
                data[x, y] = (255, 255, 255)
            if x == left or x == right or y == top or y == bottom:
                data[x, y] = (255, 255, 0)
            if (x, y) in coordinates:
                data[x, y] = color(l, cap=255)
    ax.imshow(data)


labels = (format(n, 'x') for n in count())
label = {(-1, -1): '.'}
coordinates = []
with open('coordinates.dat') as f:
    for line in f:
        x, y = line.split(',')
        coordinate = (int(x), int(y))
        label[coordinate] = next(labels)
        coordinates.append(coordinate)

left = min(x for x, _ in coordinates)
right = max(x for x, _ in coordinates)
top = min(y for _, y in coordinates)
bottom = max(y for _, y in coordinates)

grid = {}
blacklist = set()
margin = 100
for x in range(right + margin):
    for y in range(bottom + margin):
        nearest, competitor, *_ = sorted(coordinates, key=distance(x, y))
        label[(x, y)] = label.get((x, y)) or label.get(nearest).lower()
        if distance(x, y)(nearest) != distance(x, y)(competitor):
            grid[(x, y)] = nearest
        if x == left or x == right or y == top or y == bottom:
            blacklist.add(nearest)

counter = Counter(coordinate for coordinate in grid.values() if coordinate not in blacklist)
winner, count = counter.most_common(1)[0]
assert count == 3006, count
print(count)
show(winner)
plt.show()
