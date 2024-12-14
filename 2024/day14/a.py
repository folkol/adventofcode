import re
from collections import Counter
from itertools import batched

from math import prod

WIDTH, HEIGHT = 101, 103


def quadrant(x, y):
    if x == WIDTH // 2 or y == HEIGHT // 2:
        return None
    return (x > WIDTH // 2) + 2 * (y > HEIGHT // 2) + 1


with open('input.dat') as f:
    numbers = [int(x) for x in re.findall(r'-?\d+', f.read())]
    robots = [list(x) for x in batched(numbers, 4)]

for _ in range(100):
    for r in robots:
        r[0] = (r[0] + r[2]) % WIDTH
        r[1] = (r[1] + r[3]) % HEIGHT

quadrant_population = Counter(
    q
    for x, y, *_ in robots
    if (q := quadrant(x, y)) is not None
)
print(prod(quadrant_population.values()))
