DIRS = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}
WIDER = {'#': '##', '@': '@.', '.': '..', 'O': '[]'}


def valid_move(x, y, dx, dy, ):
    ny = y + dy
    nx = x + dx

    if grid[ny][nx] == '.':
        return True

    if grid[ny][nx] == '#':
        return False

    if dy == 0:
        return valid_move(nx, ny, dx, dy)
    elif grid[ny][nx] == '[':
        return valid_move(nx, ny, dx, dy) and valid_move(nx + 1, ny, dx, dy)
    elif grid[ny][nx] == ']':
        return valid_move(nx, ny, dx, dy) and valid_move(nx - 1, ny, dx, dy)

    return True


def push(x, y, dx, dy, ):
    ny = y + dy
    nx = x + dx

    if grid[ny][nx] == '.':
        grid[ny][nx], grid[y][x] = grid[y][x], grid[ny][nx]
        return nx, ny

    if dy == 0:
        push(nx, ny, dx, dy)
    elif grid[ny][nx] == '[':
        push(nx, ny, dx, dy)
        push(nx + 1, ny, dx, dy)
    elif grid[ny][nx] == ']':
        push(nx, ny, dx, dy)
        push(nx - 1, ny, dx, dy)

    grid[ny][nx], grid[y][x] = grid[y][x], grid[ny][nx]
    return nx, ny


with open("input.dat") as f:
    grid, moves = f.read().split('\n\n')

grid = [[xx for x in row for xx in WIDER[x]] for row in grid.split('\n')]
moves = [DIRS[m] for m in moves if m in '<>^v']
robot = next((x, y) for y, row in enumerate(grid) for x, v in enumerate(row) if v == '@')

for velocity in moves:
    if valid_move(*robot, *velocity):
        robot = push(*robot, *velocity)

print(sum(x + 100 * y for y, row in enumerate(grid) for x, v in enumerate(row) if v == '['))
