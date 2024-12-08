from collections import defaultdict
from itertools import permutations, combinations

with open('input.dat') as f:
    grid = [line.rstrip() for line in f]

antennas_by_frequency = defaultdict(list)
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell != '.':
            antennas_by_frequency[cell].append(x + y * 1j)


def on_grid(z):
    return 0 <= z.real < len(grid[0]) and 0 <= z.imag < len(grid)


def trace_line(z, direction):
    while on_grid(z):
        yield z
        z += direction


antinodes = {
    antinode
    for positions in antennas_by_frequency.values()
    for a, b in permutations(positions, 2)
    for antinode in trace_line(a, b - a)
}

print(len(antinodes))
