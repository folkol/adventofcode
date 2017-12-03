"""Calculates memory latency á la https://adventofcode.com/2017/day/3."""
from collections import namedtuple
from itertools import islice


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def spiral_to_cartesian():
    """Generates cartesian coordinates correponding to spirals.

    Spiral coordinates, as defined by https://adventofcode.com/2017/day/3.

    The first few looks like this:

        17  16  15  14  13
        18   5   4   3  12
        19   6   1   2  11
        20   7   8   9  10
        21  22  23---> ...
    """
    Direction = namedtuple("Direction", ['x', 'y'])
    right = Direction(1, 0)
    up = Direction(0, 1)
    left = Direction(-1, 0)
    down = Direction(0, -1)
    next_direction = {
        right: up,
        up: left,
        left: down,
        down: right
    }

    direction = right
    x, y = 0, 0
    side = 1.0
    while True:
        for _ in range(int(side)):
            yield x, y
            x += direction.x
            y += direction.y
        direction = next_direction[direction]
        side += 0.5  # we want to increase the side every other iteration


N = 312051 - 1  # 1-indexed
a_la_cartes = next(islice(spiral_to_cartesian(), N, None))
print(manhattan_distance(0, 0, *a_la_cartes))
