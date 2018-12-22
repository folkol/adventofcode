from collections import namedtuple, deque
# from dataclasses import make_dataclass
from itertools import product

Coordinate = namedtuple('Coordinate', ('x', 'y'))


# Region = make_dataclass('Region', ('type', 'index', 'erosion'))
class Region(object):
    def __init__(self, type, index, erosion):
        self.type = type
        self.index = index
        self.erosion = erosion

    def type(self):
        return self.type

    def index(self):
        return self.index

    def erosion(self):
        return self.erosion


mouth = 0, 0
depth = 8112
target = Coordinate(13, 743)
# depth = 510
# target = Coordinate(10, 10)

risk_levels = {
    'rocky': 0,
    'wet': 1,
    'narrow': 2
}
region_type = {
    0: 'rocky',
    1: 'wet',
    2: 'narrow'
}
cave = {}

# two times ought to be enough for anybody
for pos in (Coordinate(x, y) for x, y in product(range(target.y * 2), range(target.y * 2))):
    if pos in (mouth, target):
        index = 0
    elif pos.y == 0:
        index = pos.x * 16807
    elif pos.x == 0:
        index = pos.y * 48271
    else:
        index = cave[pos.x - 1, pos.y].erosion * cave[pos.x, pos.y - 1].erosion

    erosion = (index + depth) % 20183

    cave[pos] = Region(region_type[erosion % 3], index, erosion)

gear_options = {
    'rocky': {'climbing', 'torch'},
    'wet': {'climbing', 'neither'},
    'narrow': {'torch', 'neither'}
}

queue = deque()
equipped = 'torch'
queue.append(('torch', mouth, 0))
quickest = {('torch', mouth): 0}


def adjacents(pos):
    x, y = pos
    return ((x + dx, y + dy)
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]
            if (x + dx) >= 0 and (y + dy) >= 0)


def enqueue(to, equipped, time):
    if ('torch', target) in quickest and time > quickest[('torch', target)]:
        return
    if (equipped, to) not in quickest or quickest[(equipped, to)] > time:
        queue.append((equipped, to, time))
        for gear in gear_options[cave[to].type]:
            dtime = time if gear == equipped else time + 7
            if (equipped, to) not in quickest or quickest[(equipped, to)] > dtime:
                quickest[(equipped, to)] = dtime


print('Searching')
seen = set()
n = 0
while queue:
    equipped, coordinate, time = queue.popleft()
    if n % 10000 == 0:
        print(len(queue), coordinate[0], coordinate[1], equipped)
    n += 1

    if coordinate == target:
        dtime = time if equipped == 'torch' else time + 7
        if ('torch', target) in quickest and quickest[('torch', target)] > dtime:
            quickest[('torch', target)] = dtime

    for adjacent in adjacents(coordinate):
        if equipped in gear_options[cave[adjacent].type]:
            enqueue(adjacent, equipped, time + 1)
    for gear in gear_options[cave[coordinate].type]:
        if gear != equipped:
            enqueue(coordinate, gear, time + 7)

print(quickest[('torch', target)])
