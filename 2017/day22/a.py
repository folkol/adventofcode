UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

turn_left = {
    UP: LEFT,
    DOWN: RIGHT,
    LEFT: DOWN,
    RIGHT: UP
}
turn_right = {
    UP: RIGHT,
    DOWN: LEFT,
    LEFT: UP,
    RIGHT: DOWN
}

data = [list(line.strip()) for line in open('map.dat')]

x, y = 0, 0
direction = UP
size = len(data)  # Assume square grid
grid = {
    (col - size // 2, row - size // 2): state
    for row, line in enumerate(data)
    for col, state in enumerate(line)
}


def print_grid():
    mincol = min(col for col, _ in grid)
    maxcol = max(col for col, _ in grid)
    minrow = min(row for _, row in grid)
    maxrow = max(row for _, row in grid)
    for i in range(minrow, maxrow + 1):
        for j in range(mincol, maxcol + 1):
            if (j, i) == (x, y):
                sep = ']'
            elif (j, i) == (x - 1, y):
                sep = '['
            else:
                sep = ' '

            print(grid.get((j, i), '.'), end=sep)
        print()


num_infected = 0
for _ in range(10_000):
    current = grid.get((x, y), '.')
    if current == '#':
        direction = turn_right[direction]
    else:
        direction = turn_left[direction]
    if current == '.':
        grid[x, y] = '#'
        num_infected += 1
    else:
        grid[x, y] = '.'
    x += direction[0]
    y += direction[1]

print_grid()
print(num_infected)
