import heapq
import math
from collections import defaultdict, deque

with open("input.dat") as f:
    maze = f.read().splitlines()


def routes(x, y, direction):
    dy, dx = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}[direction]
    if maze[y + dy][x + dx] != "#":
        yield 1, (x + dx, y + dy, direction)
    yield 1000, (x, y, (direction - 1) % 4)
    yield 1000, (x, y, (direction + 1) % 4)


S, E = (len(maze) - 2, 1, 1), (1, len(maze[0]) - 2)
queue, lowest_score = [(0, S)], {S: 0}
parents = defaultdict(set)
while queue:
    score, orientation = heapq.heappop(queue)
    for weight, route in routes(*orientation):
        if score + weight < lowest_score.get(route, math.inf):
            lowest_score[route] = score + weight
            heapq.heappush(queue, ((score + weight), route))
            parents[route] = {orientation}
        elif score + weight == lowest_score.get(route, math.inf):
            parents[route].add(orientation)

queue = deque(p for p in parents if p[:2] == E)
tiles = set()
while queue:
    pos = queue.popleft()
    tiles.add(pos)
    queue.extend(p for p in parents[pos])

print(len({t[:2] for t in tiles}))
