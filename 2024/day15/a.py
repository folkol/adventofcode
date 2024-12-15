def move_to_dir(m):
    dirs = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}
    return dirs[m]


with open("input.dat") as f:
    grid, moves = f.read().split('\n\n')
    grid = [list(row) for row in grid.split('\n')]
    moves = [(m, move_to_dir(m)) for m in moves if m in '<>^v']
    robot = next((x, y) for y, row in enumerate(grid) for x, v in enumerate(row) if v == '@')


def attempt(x, y, dx, dy):
    if grid[y + dy][x + dx] == '.':
        grid[y + dy][x + dx], grid[y][x] = grid[y][x], grid[y + dy][x + dx]
        return x + dx, y + dy
    if grid[y + dy][x + dx] == '#':
        return x, y
    attempt(x + dx, y + dy, dx, dy)
    if grid[y + dy][x + dx] == '.':
        return attempt(x, y, dx, dy)
    return x, y


for move, velocity in moves:
    robot = attempt(*robot, *velocity)

print(sum(
    x + 100 * y
    for y, row in enumerate(grid)
    for x, v in enumerate(row)
    if v == 'O'
))
