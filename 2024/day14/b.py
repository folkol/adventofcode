import re
from collections import Counter
from itertools import batched, count

WIDTH, HEIGHT = 101, 103
SCIENTIFICALLY_ACCURATE_MAGIC_NUMBER = 1337


def quadrant(x, y):
    if x == WIDTH // 2 or y == HEIGHT // 2:
        return None
    return (x > WIDTH // 2) + 2 * (y > HEIGHT // 2) + 1


with open('input.dat') as f:
    numbers = [int(x) for x in re.findall(r'-?\d+', f.read())]
    robots = [list(x) for x in batched(numbers, 4)]

robots_here = Counter((x, y) for x, y, *_ in robots)


def nearby_robots(x, y):
    return sum(robots_here[x + dx, y + dy] for dx in [-1, 0, 1] for dy in [-1, 0, 1])

def maybe_tree():
    robots_with_friends = sum(nearby_robots(x, y) for x, y, *_ in robots)
    return robots_with_friends > SCIENTIFICALLY_ACCURATE_MAGIC_NUMBER


def print_grid():
    for y in range(HEIGHT):
        print(*('X' if nearby_robots(x, y) > 1 else '.' for x in range(WIDTH)))
    print()


for n in count():
    if maybe_tree():
        print('Maybe tree after', n, 'ticks?')
        print_grid()
    for r in robots:
        robots_here[(r[0], r[1])] -= 1
        r[0] = (r[0] + r[2]) % WIDTH
        r[1] = (r[1] + r[3]) % HEIGHT
        robots_here[(r[0], r[1])] += 1
