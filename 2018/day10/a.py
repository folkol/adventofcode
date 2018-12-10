import re
from collections import defaultdict
from itertools import count

import matplotlib.pyplot as plt
import numpy as np

coordinates = []
with open('points.dat') as f:
    for line in f:
        match = re.match('position=<(.*), (.*)> velocity=<(.*),(.*)>', line)
        x, y, dx, dy = (int(g) for g in match.groups())
        coordinates.append((x, y, dx, dy))


def is_message(coordinates):
    """Tries to identify a message in the list of points by looking for a vertical line."""
    points = defaultdict(list)
    for x, y, *_ in coordinates:
        points[x].append(y)
    for x, ys in sorted(points.items()):
        prev = None
        consecutive = 1
        for y in sorted(ys):
            if prev is None or y == (prev + 1):
                consecutive += 1
                if consecutive > 8:
                    return True
            prev = y


def print_message(coordinates):
    points = {(x, y) for x, y, dx, dy in coordinates}

    fig, ax = plt.subplots()
    min_x = min(x for x, y, dx, dy in coordinates)
    max_x = max(x for x, y, dx, dy in coordinates)
    min_y = min(y for x, y, dx, dy in coordinates)
    max_y = max(y for x, y, dx, dy in coordinates)
    print(min_x, max_x, min_y, max_y)
    data = np.zeros((max_y - min_y + 1, max_x - min_x + 1, 3)).astype(np.uint8)
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) in points:
                data[y - min_y, x - min_x] = (255, 255, 255)
            else:
                data[y - min_y, x - min_x] = (0, 0, 0)
    ax.imshow(data)
    plt.pause(0.01)
    plt.show()


for n in count():
    if is_message(coordinates):
        print('Found message at iteration', n)
        print_message(coordinates)
        break
    coordinates = [(x + dx, y + dy, dx, dy) for x, y, dx, dy in coordinates]
    print(n)
