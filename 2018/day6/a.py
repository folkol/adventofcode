import heapq
from collections import Counter
from itertools import cycle, count
from string import ascii_uppercase

import matplotlib.pyplot as plt
import numpy as np

winner = None
margin = 100
def manhattan(x1, y1):
    def inner(coordinate):
        x2, y2 = coordinate
        return abs(x2 - x1) + abs(y2 - y1)

    return inner


labels = (format(n, 'x') for n in count())
label = {}
label[(-1, -1)] = '.'
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

print(left, right, top, bottom)

grid = {}
blacklist = set()

for coordinate in coordinates:
    label[coordinate] = label[coordinate]

fig, ax = plt.subplots()

data = []


def show():
    def color(l):
        cap = 255
        l = l.upper()
        return (int(l, 16) * 17) % cap, (int(l, 16) * 17 * 17) % cap, (int(l, 16) * 17 * 17 * 17) % cap

    data = np.zeros((right + margin, bottom + margin, 3)).astype(np.uint8)
    for x in range(right + margin):
        for y in range(bottom + margin):
            l = label.get((x, y))
            if l:
                data[x, y] = color(l)
            if x == left or x == right or y == top or y == bottom:
                data[x, y] = (255, 255, 0)
            if (x, y) in coordinates:
                data[x, y] = (0, 255, 0)
            if winner and label.get((x, y)) == label.get(winner).lower():
                data[x, y] = (255, 255, 255)


    ax.cla()
    ax.imshow(data)
    plt.pause(0.00001)


for x in range(right + margin):
    for y in range(bottom + margin):
        nearest, competitor, *_ = sorted(coordinates, key=manhattan(x, y))
        label[(x, y)] = label.get((x, y)) or label.get(nearest).lower()
        if manhattan(x, y)(nearest) != manhattan(x, y)(competitor):
            grid[(x, y)] = nearest
        # else:
        #     print('No nearest:', (x, y), competitor)

        if x == left or x == right or y == top or y == bottom:
            blacklist.add(nearest)
    if not x % 10:
        # show()
        pass

counter = Counter(coordinate for coordinate in grid.values() if coordinate not in blacklist)
common = counter.most_common(1)
winner = common[0][0]
print(common, winner)
show()
plt.show()
