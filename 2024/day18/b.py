from collections import deque
from itertools import count

N = 70

with (open('input.dat') as f):
    coords = [(int(x), int(y)) for line in f for x, y in [line.split(',')]]

for n in count():
    print('Trying', n, coords[n])

    is_corrupted = coords[:n]


    def valid_step(x, y):
        return 0 <= x <= N and 0 <= y <= N and (x, y) not in is_corrupted


    path_found = False
    queue = deque([(0, 0, 0)])
    seen = set()
    while queue:
        x, y, steps = queue.popleft()
        if (x, y) == (N, N):
            path_found = True
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if valid_step(nx, ny) and (nx, ny) not in seen:
                seen.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    if not path_found:
        print('Path blocked!', n - 1, coords[n - 1])
        break
