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

cave = {}

print('Generating map...')
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


def adjacents(pos):
    x, y = pos
    return ((x + dx, y + dy)
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]
            if (x + dx) >= 0 and (y + dy) >= 0)


def enqueue(to, equipped, time):
    if ('torch', TARGET) in quickest and time > quickest[('torch', TARGET)]:
        return
    if (equipped, to) not in quickest or quickest[(equipped, to)] > time:
        heappush(queue, (time, to, equipped))
        for gear in GEAR_OPTIONS[cave[to].type]:
            dtime = time if gear == equipped else time + 7
            if (equipped, to) not in quickest or quickest[(equipped, to)] > dtime:
                quickest[(equipped, to)] = dtime


print('Searching...')
queue = []
quickest = {}
enqueue((0, 0), 'torch', 0)
while queue:
    time, coordinate, equipped = heappop(queue)

    if coordinate == TARGET:
        dtime = time if equipped == 'torch' else time + 7
        if ('torch', TARGET) in quickest and quickest[('torch', TARGET)] > dtime:
            quickest[('torch', TARGET)] = dtime

    for adjacent in adjacents(coordinate):
        if equipped in GEAR_OPTIONS[cave[adjacent].type]:
            enqueue(adjacent, equipped, time + 1)
    for gear in GEAR_OPTIONS[cave[coordinate].type]:
        if gear != equipped:
            enqueue(coordinate, gear, time + 7)

print(quickest[('torch', TARGET)])
