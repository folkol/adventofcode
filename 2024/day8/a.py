from collections import defaultdict
from itertools import permutations

with open('input.dat') as f:
    grid = [line.rstrip() for line in f]

width, height = len(grid[0]), len(grid)

antennas = defaultdict(list)
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell != '.':
            antennas[cell].append(x + y * 1j)

antinodes = {
    a + (b - a) * -1
    for positions in antennas.values()
    for a, b in permutations(positions, 2)
}

print(sum(0 <= a.real < width and 0 <= a.imag < height for a in antinodes))
