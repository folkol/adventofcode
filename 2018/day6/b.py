from collections import deque


def distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def within_region(k):
    cumulative_distance = 0
    for c in coordinates:
        cumulative_distance += distance(*k, *c)
        if cumulative_distance >= 10_000:
            return False
    return True


coordinates = []
with open('coordinates.dat') as f:
    for line in f:
        x, y = line.split(',')
        coordinates.append((int(x), int(y)))

center = sum(x for x, _ in coordinates) // len(coordinates), sum(y for _, y in coordinates) // len(coordinates)

seen = {center}
size = 1
queue = deque()
queue.append(center)
while queue:
    x, y = queue.pop()
    for candidate in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if candidate not in seen:
            seen.add(candidate)
            if within_region(candidate):
                queue.append(candidate)
                size += 1
print(size)
