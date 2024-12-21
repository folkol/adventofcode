import heapq
import math

with open("input.dat") as f:
    maze = f.read().splitlines()


def routes(y, x, direction):
    dy, dx = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}[direction]
    if maze[y + dy][x + dx] != "#":
        yield 1, (y + dy, x + dx, direction)
    yield 1000, (y, x, (direction - 1) % 4)
    yield 1000, (y, x, (direction + 1) % 4)


S, E = (len(maze) - 2, 1, 1), [1, len(maze[0]) - 2]
queue, lowest_score = [(0, S)], {S: 0}
while queue:
    score, orientation = heapq.heappop(queue)
    for weight, route in routes(*orientation):
        if score + weight < lowest_score.get(route, math.inf):
            lowest_score[route] = score + weight
            heapq.heappush(queue, (score + weight, route))

print(next(cost for (*pos, _), cost in lowest_score.items() if pos == E))
