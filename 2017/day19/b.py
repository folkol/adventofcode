from collections import namedtuple
from string import ascii_uppercase
from itertools import count

Direction = namedtuple('Direction', ['dx', 'dy'])
UP = Direction(0, -1)
DOWN = Direction(0, 1)
LEFT = Direction(-1, 0)
RIGHT = Direction(1, 0)

turn_left = {UP: LEFT, DOWN: RIGHT, LEFT: DOWN, RIGHT: UP}
turn_right = {UP: RIGHT, DOWN: LEFT, LEFT: UP, RIGHT: DOWN}

diagram = [list(row.strip('\n')) for row in open('diagram.dat')]

x, y = diagram[0].index('|'), -1
direction = DOWN

seen = []
for steps in count():
    if diagram[y][x] in ascii_uppercase:
        seen.append(diagram[y][x])

    x, y = x + direction.dx, y + direction.dy
    if diagram[y][x] == ' ':
        break
    elif diagram[y][x] == '+':
        direction = turn_left[direction]
        if diagram[y + direction.dy][x + direction.dx] == ' ':
            direction = turn_right[direction]
            direction = turn_right[direction]

print(steps)
