from collections import namedtuple
from dataclasses import make_dataclass
from heapq import heappop, heappush
from itertools import product

Coordinate = namedtuple('Coordinate', ('x', 'y'))
Region = make_dataclass('Region', ('type', 'index', 'erosion'))

MOUTH = 0, 0
DEPTH = 8112
TARGET = Coordinate(13, 743)
# DEPTH = 510
# TARGET = Coordinate(10, 10)

REGION_TYPE = {
    0: 'rocky',
    1: 'wet',
    2: 'narrow'
}

GEAR_OPTIONS = {
    'rocky': {'climbing', 'torch'},
    'wet': {'climbing', 'neither'},
    'narrow': {'torch', 'neither'}
}

print('Generating map...')
cave = {}
for pos in (Coordinate(x, y) for x, y in product(range(TARGET.y + 50), range(TARGET.y + 50))):
    if pos in (MOUTH, TARGET):
        index = 0
    elif pos.y == 0:
        index = pos.x * 16807
    elif pos.x == 0:
        index = pos.y * 48271
    else:
        index = cave[pos.x - 1, pos.y].erosion * cave[pos.x, pos.y - 1].erosion

    erosion = (index + DEPTH) % 20183
    cave[pos] = Region(REGION_TYPE[erosion % 3], index, erosion)


def adjacents(x, y):
    return ((x + dx, y + dy)
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]
            if (x + dx) >= 0 and (y + dy) >= 0)


def enqueue(destination, equipped, time):
    if quickest.get(('torch', TARGET), time) < time:
        return
    to = (equipped, destination)
    if quickest.get(to, time + 1) > time:
        heappush(queue, (time, destination, equipped))
        quickest[to] = time


print('Searching...')
queue = []
quickest = {}
enqueue((0, 0), 'torch', 0)
while queue:
    time, coordinate, equipped = heappop(queue)
    for adjacent in adjacents(*coordinate):
        if equipped in GEAR_OPTIONS[cave[adjacent].type]:
            enqueue(adjacent, equipped, time + 1)
    for gear in GEAR_OPTIONS[cave[coordinate].type]:
        if gear != equipped:
            enqueue(coordinate, gear, time + 7)

print(quickest[('torch', TARGET)])
