from collections import deque

with open('input.dat') as f:
    grid = f.read().splitlines()

sx, sy = next((x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == 'S')
ex, ey = next((x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == 'E')


def manhattan_distance(x, y, i, j):
    return abs(i - x) + abs(j - y)


def trace_path():
    queue = deque([(sx, sy)])
    seen = {(sx, sy)}
    while queue:
        x, y = queue.popleft()
        yield x, y
        for nx, ny in [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]:
            if grid[ny][nx] != '#' and (nx, ny) not in seen:
                queue.append((nx, ny))
                seen.add((nx, ny))


path = list(trace_path())
num_cheats = sum(
    manhattan_distance(*path[start], *path[end]) <= 2
    for start in range(len(path) - 100)
    for end in range(start + 102, len(path))
)
print(num_cheats)
