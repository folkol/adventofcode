import re
from collections import defaultdict


def travel(n, nodes, seen):
    """Recursively visits every node in the graph defined by edges.

    The visited nodes will be accumulated in the set 'seen'.
    """
    for node in nodes[n]:
        if node not in seen:
            seen.add(node)
            travel(node, nodes, seen)


# Builds up an adjacency list
nodes = defaultdict(list)
for line in open('connections.dat'):
    node, *neighbours = re.findall('\d+', line)
    for neighbour in neighbours:
        nodes[node].append(neighbour)
        nodes[neighbour].append(node)

group = set()
travel('0', nodes, group)
print(len(group))
