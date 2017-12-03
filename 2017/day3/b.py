"""Calculates memory latency á la https://adventofcode.com/2017/day/3."""
from collections import namedtuple

Direction = namedtuple("Direction", ['x', 'y'])
RIGHT = Direction(1, 0)
UP = Direction(0, 1)
LEFT = Direction(-1, 0)
DOWN = Direction(0, -1)
next_direction = {
    RIGHT: UP,
    UP: LEFT,
    LEFT: DOWN,
    DOWN: RIGHT
}


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
    direction = RIGHT
    x, y = 0, 0
    side = 1.0
    while True:
        for _ in range(int(side)):
            yield x, y
            x += direction.x
            y += direction.y
        direction = next_direction[direction]
        side += 0.5  # we want to increase the side every other iteration


def neighbour_sum(x, y):
    value = 0
    value += values.get((x - 1, y - 1), 0)
    value += values.get((x, y - 1), 0)
    value += values.get((x + 1, y - 1), 0)
    value += values.get((x - 1, y), 0)
    value += values.get((x, y), 0)
    value += values.get((x + 1, y), 0)
    value += values.get((x - 1, y + 1), 0)
    value += values.get((x, y + 1), 0)
    value += values.get((x + 1, y + 1), 0)
    return value


values = {
    (0, 0): 1
}
N = 312051
for x, y in spiral_to_cartesian():
    value = neighbour_sum(x, y)
    values[(x, y)] = value
    if value > N:
        print(value)
        break
