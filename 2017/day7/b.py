"""Searches for the node with the wrong weight.

    Unbalanced nodes are nodes with a recursive weight that differs
    from its siblings.

    From these nodes, the one with balanced children is the one with
    the wrong weight.

    Todo: Add proper data structures to avoid looksups all the time.
"""
import re
from collections import defaultdict, Counter


class Node(object):
    def total_weight(self):
        """Recursively calculate the weight for all programs in this node."""
        return self.weight + sum(child.total_weight() for child in self.children)

    def __init__(self):
        self.name = 'unknown'
        self.weight = 0
        self.parent = None
        self.children = []


nodes = defaultdict(Node)
# for line in stdin:
for line in open('programs.dat'):
    name, weight, *children = re.findall('\w+', line)
    node = nodes[name]
    node.name = name
    node.weight = int(weight)
    for child in children:
        child_node = nodes[child]
        child_node.parent = node
        child_node.name = child
        node.children.append(nodes[child])


def unbalanced(children):
    counter = Counter(child.total_weight() for child in children)
    if len(counter) == 1:
        return None
    (mode, _), (wrong, _) = counter.most_common()
    for child in children:
        if child.total_weight() == wrong:
            return child


for name, node in nodes.items():
    if node.parent and node == unbalanced(node.parent.children) and not unbalanced(node.children):
        counter = Counter(child.total_weight() for child in node.parent.children)
        (mode, _), *_ = counter.most_common()
        print(mode)
