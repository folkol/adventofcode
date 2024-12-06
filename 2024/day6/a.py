TURN_RIGHT = {"^": ">", ">": "v", "v": "<", "<": "^"}
DIRECTIONS = {"^": (0, -1), "v": (0, 1), ">": (1, 0), "<": (-1, 0)}

with open("input.dat") as f:
    grid = [list(row.rstrip()) for row in f]

y, x = next((y, x) for y, row in enumerate(grid) for x, e in enumerate(row) if e == "^")
grid[y][x] = "."
direction = "^"


def inside(x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


visited = set()
while inside(x, y):
    visited.add((x, y))
    dx, dy = DIRECTIONS[direction]
    next_x, next_y = x + dx, y + dy
    if inside(next_x, next_y) and grid[next_y][next_x] == "#":
        direction = TURN_RIGHT[direction]
        continue
    x, y = next_x, next_y

print(len(visited))
