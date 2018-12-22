from collections import namedtuple
from dataclasses import make_dataclass

Coordinate = namedtuple('Coordinate', ('x', 'y'))
Region = make_dataclass('Region', ('type', 'index', 'erosion'))

depth = 8112
target = Coordinate(13, 743)
# depth = 510
# target = Coordinate(10, 10)

cave = {}
for pos in (Coordinate(x, y) for y in range(target.y + 1) for x in range(target.x + 1)):
    if pos == (0, 0):
        index = 0
    elif pos == target:
        index = 0
    elif pos.y == 0:
        index = pos.x * 16807
    elif pos.x == 0:
        index = pos.y * 48271
    else:
        index = cave[Coordinate(pos.x - 1, pos.y)].erosion * cave[Coordinate(pos.x, pos.y - 1)].erosion

    erosion = (index + depth) % 20183

    if erosion % 3 == 0:
        region = 'rocky'
    elif erosion % 3 == 1:
        region = 'wet'
    else:
        region = 'narrow'

    cave[pos] = Region(region, index, erosion)

# for y in range(target[1] + 1 + 5):
#     for x in range(target[0] + 1 + 5):
#         pos = Coordinate(x, y)
#         if pos == (0, 0):
#             print('M', end='')
#         elif pos == target:
#             print('T', end='')
#         elif cave[pos].type == 'rocky':
#             print('.', end='')
#         elif cave[pos].type == 'wet':
#             print('=', end='')
#         else:
#             print('|', end='')
#     print()

risk_levels = {
    'rocky': 0,
    'wet': 1,
    'narrow': 2
}
print(sum(risk_levels[region.type] for region in cave.values()))
