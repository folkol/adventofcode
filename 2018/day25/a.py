from collections import deque

with open('fixpoints.dat') as f:
    fixpoints = [tuple(int(p) for p in line.strip().split(',')) for line in f]


def manhattan(node, p):
    return abs(node[0] - p[0]) + abs(node[1] - p[1]) + abs(node[2] - p[2]) + abs(node[3] - p[3])


constallations = []

while fixpoints:
    constellation = []
    q = deque()
    root = fixpoints[0]
    q.append(root)
    visited = {root}
    while q:
        node = q.popleft()
        constellation.append(node)
        for p in fixpoints:
            if manhattan(node, p) <= 3 and p not in visited:
                visited.add(p)
                q.append(p)
    constallations.append(constellation)
    for p in constellation:
        fixpoints.remove(p)
print(constallations)
print(len(constallations))
