with open('input.dat') as f:
    grid = {
        x + y * 1j: int(h)
        for y, line in enumerate(f)
        for x, h in enumerate(line.rstrip())
    }


def slope(cur, dest):
    if dest_height := grid.get(dest):
        return dest_height - grid[cur]


def trailhead_score(start):
    peaks, queue = set(), [start]
    while p := queue.pop() if queue else None:
        if grid[p] == 9:
            peaks.add(p)
        queue.extend(p + n for n in [-1, 1, -1j, 1j] if slope(p, p + n) == 1)
    return len(peaks)


print(sum(trailhead_score(z) for z in grid if grid[z] == 0))
