"""Finds the solution for https://adventofcode.com/2017/day/7.

    Constructs a tree graph of the nodes read from stdin, finds the node with
    a divergent weight and prints its ideal weight to stdout.

    The tree is defined by a number of lines such as this one:

        name (weight) -> child1, child2...
"""
import re
from collections import defaultdict, Counter


class Node(object):
    def __init__(self):
        self.name = 'unknown'
        self.weight = 0
        self.parent = None
        self.children = []

    def total_weight(self):
        return self.weight + sum(child.total_weight() for child in self.children)


def read_graph(f):
    graph = defaultdict(Node)
    for line in f:
        name, weight, *children = re.findall('\w+', line)
        node = graph[name]
        node.name = name
        node.weight = int(weight)
        for c in children:
            child = graph[c]
            child.parent = node
            child.name = c
            node.children.append(child)
    return dict(graph)


def deviant(children):
    """Returns the deviant – as in weigh – child, if any."""
    weights = Counter(child.total_weight() for child in children)
    if len(weights) == 1:
        return None
    (mode, _), (outlier, _) = weights.most_common()
    return next(child for child in children if child.total_weight() == outlier)


# programs = read_graph(stdin)
family = read_graph(open('programs.dat'))
for program in family.values():
    if not program.parent:
        # In solitude, balance!
        continue

    # A deviant node with no deviant children is the black sheep.
    siblings = program.parent.children
    if program is deviant(siblings) and None is deviant(program.children):
        counter = Counter(child.total_weight() for child in siblings)
        (ideal_weight, _), *_ = counter.most_common()
        assert ideal_weight == 1486, 'You broke it!'
        print(ideal_weight)
