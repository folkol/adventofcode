from collections import defaultdict

grid = defaultdict(dict)
velocity = {
    'U': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
    'D': (0, 1),
}

def trace(grid, i, steps):
    x, y = 0, 0
    num_steps = 0
    for step in steps:
        direction, distance = step[0], int(step[1:])
        print(direction, distance)
        dx, dy = velocity[direction]
        for n in range(distance):
            x, y = x + dx, y + dy
            num_steps += 1
            if i not in grid[(x, y)]:
                grid[(x, y)][i] = num_steps

def manhattan_distance(x, y):
    return abs(x) + abs(y)

with open('input.dat') as f:
    for i, line in enumerate(f):
        trace(grid, i, line.split(','))
    collisions = (
        steps[0] + steps[1]
        for coordinates, steps
        in grid.items()
        if len(steps) > 1)
    print(min(collisions))