from collections import deque

with open('fixpoints.dat') as f:
    fixpoints = [tuple(int(p) for p in line.strip().split(',')) for line in f]


def manhattan(a, b):
    return sum(abs(i - j) for i, j in zip(a, b))


def get_constallation():
    constellation = []
    q = deque()
    root = fixpoints[0]
    q.append(root)
    visited = {root}
    while q:
        node = q.popleft()
        constellation.append(node)
        for fixpoint in fixpoints:
            if manhattan(node, fixpoint) <= 3 and fixpoint not in visited:
                visited.add(fixpoint)
                q.append(fixpoint)
    return constellation


constallations = []
while fixpoints:
    constellation = get_constallation()
    constallations.append(constellation)
    fixpoints = [p for p in fixpoints if p not in constellation]
print(len(constallations))
