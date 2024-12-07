TURN_RIGHT = {"^": ">", ">": "v", "v": "<", "<": "^"}
DIRECTIONS = {"^": (0, -1), "v": (0, 1), ">": (1, 0), "<": (-1, 0)}

with open("input.dat") as f:
    grid = [list(row.rstrip()) for row in f]


def inside_grid(x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def grid_at(next_x, next_y):
    return inside_grid(next_x, next_y) and grid[next_y][next_x]


def grid_has_cycle():
    direction = '^'
    [x, y], [dx, dy] = starting_point, DIRECTIONS[direction]
    visited = set()
    while inside_grid(x, y) and (x, y, direction) not in visited:
        visited.add((x, y, direction))
        next_x, next_y = x + dx, y + dy
        if grid_at(next_x, next_y) == "#":
            direction = TURN_RIGHT[direction]
            dx, dy = DIRECTIONS[direction]
        else:
            x, y = next_x, next_y
    return (x, y, direction) in visited


starting_point = next((x, y) for y, row in enumerate(grid) for x, e in enumerate(row) if e == "^")
direction = '^'
[x, y], [dx, dy] = starting_point, DIRECTIONS[direction]
candidates = set()
while inside_grid(x, y):
    next_x, next_y = x + dx, y + dy
    if grid_at(next_x, next_y) == ".":
        grid[next_y][next_x] = "#"
        if grid_has_cycle():
            candidates.add((next_x, next_y))
        grid[next_y][next_x] = "."
    if grid_at(next_x, next_y) == "#":
        direction = TURN_RIGHT[direction]
        dx, dy = DIRECTIONS[direction]
        continue
    else:
        x, y = next_x, next_y

print(len(candidates))
