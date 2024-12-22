from collections import deque

N = 70

with (open('input.dat') as f):
    is_corrupted = [(int(x), int(y)) for line in f for x, y in [line.split(',')]][:1024]


def valid_step(x, y):
    return 0 <= x <= N and 0 <= y <= N and not (x, y) in is_corrupted


queue = deque([(0, 0, 0)])
seen = set()
while queue:
    x, y, steps = queue.popleft()
    if (x, y) == (N, N):
        print(steps)
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if valid_step(nx, ny) and (nx, ny) not in seen:
            seen.add((nx, ny))
            queue.append((nx, ny, steps + 1))
