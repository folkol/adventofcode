import re
from collections import defaultdict
from itertools import count

coordinates = []
with open('points.dat') as f:
    for line in f:
        match = re.match('position=<(.*), (.*)> velocity=<(.*),(.*)>', line)
        x, y, dx, dy = (int(g) for g in match.groups())
        coordinates.append((x, y, dx, dy))


def is_message(coordinates):
    """Tries to identify a message in the swarm of points by looking for a vertical line."""
    points = defaultdict(list)
    for x, y, *_ in coordinates:
        points[x].append(y)
    for x, ys in points.items():
        prev = None
        consecutive = 1
        for y in sorted(ys):
            if prev is None or y == prev + 1:
                consecutive += 1
                if consecutive > 8:
                    return True
            prev = y


def print_message(coordinates):
    points = {(x, y) for x, y, dx, dy in coordinates}

    min_x = min(x for x, y, dx, dy in coordinates)
    max_x = max(x for x, y, dx, dy in coordinates)
    min_y = min(y for x, y, dx, dy in coordinates)
    max_y = max(y for x, y, dx, dy in coordinates)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print('*' if (x, y) in points else ' ', end='')
        print()


for n in count():
    if is_message(coordinates):
        print(f'Found message after {n} iterations:')
        print_message(coordinates)
        break
    coordinates = [(x + dx, y + dy, dx, dy) for x, y, dx, dy in coordinates]
