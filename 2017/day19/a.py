from collections import namedtuple
from string import ascii_uppercase

Direction = namedtuple('Direction', ['dx', 'dy'])
UP = Direction(0, -1)
DOWN = Direction(0, 1)
LEFT = Direction(-1, 0)
RIGHT = Direction(1, 0)

left = {
    UP: LEFT,
    DOWN: RIGHT,
    LEFT: DOWN,
    RIGHT: UP
}

right = {
    UP: RIGHT,
    DOWN: LEFT,
    LEFT: UP,
    RIGHT: DOWN
}

diagram = [list(row.strip('\n')) for row in open('diagram.dat')]
# diagram = [list(row.strip('\n')) for row in open('example.dat')]
x, y = diagram[0].index('|'), -1
direction = DOWN

seen = []



while True:
    # print(x, y)
    # print('\n'.join(row for row in (''.join(cs) for cs in diagram)))
    point = diagram[y][x]
    if point in ascii_uppercase:
        seen.append(point)

    next_x, next_y = x + direction.dx, y + direction.dy
    ahead = diagram[next_y][next_x]
    if ahead in '-|' + ascii_uppercase:
        x, y = next_x, next_y
    elif ahead == '+':
        x, y = next_x, next_y
        next_direction = left[direction]
        if diagram[y + next_direction.dy][x + next_direction.dx] not in '-|' + ascii_uppercase:
            next_direction = right[direction]
        direction = next_direction
    else:
        break
print(''.join(seen))
