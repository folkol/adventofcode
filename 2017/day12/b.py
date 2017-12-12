import re
from collections import defaultdict


def travel(n, edges, seen):
    """Recursively visits every node in the graph defined by edges.

    The visited nodes will be accumulated in the set 'seen'.
    """
    for neighbour in edges[n]:
        if neighbour not in seen:
            seen.add(neighbour)
            travel(neighbour, edges, seen)


# Builds up an adjacency list by reading connections.dat
edges = defaultdict(list)
for line in open('connections.dat'):
    node, *neighbours = re.findall('\d+', line)
    for neighbour in neighbours:
        edges[node].append(neighbour)
        edges[neighbour].append(node)


num_groups = 0

seen = set()
while len(set(edges) - set(seen)):
    unseen = next(iter(set(edges) - set(seen)))
    travel(unseen, edges, seen)
    num_groups += 1

print(num_groups)
