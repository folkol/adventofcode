from collections import namedtuple
from dataclasses import make_dataclass
from itertools import product

Coordinate = namedtuple('Coordinate', ('x', 'y'))
Region = make_dataclass('Region', ('type', 'index', 'erosion'))

mouth = 0, 0
depth = 8112
target = Coordinate(13, 743)

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
for pos in (Coordinate(x, y) for x, y in product(range(target.x + 1), range(target.y + 1))):
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

print(sum(risk_levels[region.type] for region in cave.values()))
