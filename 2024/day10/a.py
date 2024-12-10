NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
with open('input.dat') as f:
    grid = [[int(x) for x in line.rstrip()] for line in f]


def on_map(x, y):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def slope(cur_x, cur_y, dest_x, dest_y):
    if on_map(dest_x, dest_y):
        return grid[dest_y][dest_x] - grid[cur_y][cur_x]


def trailhead_score(x, y):
    seen = set()
    peaks = set()
    queue = [(x, y)]
    while queue:
        cur_x, cur_y = queue.pop()
        if grid[cur_y][cur_x] == 9:
            peaks.add((cur_x, cur_y))
            continue
        for dx, dy in NEIGHBORS:
            candidate = cur_x + dx, cur_y + dy
            if candidate not in seen and slope(cur_x, cur_y, *candidate) == 1:
                queue.append(candidate)
    return len(peaks)


scores = [
    trailhead_score(x, y)
    for y, row in enumerate(grid) for x, _ in
    enumerate(row) if grid[y][x] == 0
]

print(sum(scores))
