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


# Builds up an adjacency list by reading connections.dat
nodes = defaultdict(list)
for line in open('connections.dat'):
    node, *neighbours = re.findall('\d+', line)
    nodes[node].extend(neighbours)

num_groups = 0
seen = set()
while len(set(nodes) - set(seen)):
    unseen = next(n for n in nodes if n not in seen)
    travel(unseen, nodes, seen)
    num_groups += 1

print(num_groups)
