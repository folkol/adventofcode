from collections import deque


def in_bounds(height_map, ni, nj):
    return 0 <= ni < len(height_map) and 0 <= nj < len(height_map[0])


def fill_basin(pos, height_map):
    seen, q = set(), deque([pos])
    while q:
        current = q.popleft()
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = current[0] + di, current[1] + dj
            if in_bounds(height_map, ni, nj) and height_map[ni][nj] != 9:
                neighbour = (ni, nj)
                if neighbour not in seen:
                    q.append(neighbour)
                    height_map[ni][nj] = 9
                    seen.add(neighbour)

    return len(seen)


with open('input.dat') as f:
    height_map = [
        [int(c) for c in line.rstrip()]
        for line in f
    ]

    basins = []
    for i, row in enumerate(height_map):
        for j, _, in enumerate(row):
            if height_map[i][j] != 9:
                basins.append(fill_basin((i, j), height_map))

    basins = sorted(basins)
    print(basins[-3] * basins[-2] * basins[-1])
