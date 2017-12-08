"""Searches for the node with the wrong weight.

    Unbalanced nodes are nodes with a recursive weight that differs
    from its siblings.

    From these nodes, the one with balanced children is the one with
    the wrong weight.

    Todo: Add proper data structures to avoid looksups all the time.
"""
import re
from collections import defaultdict, Counter
from sys import stdin

nodes = defaultdict(lambda: dict(name='', weight=0, children=[]))
for line in stdin:
    name, weight, *children = re.findall('\w+', line)
    node = nodes[name]
    node['name'] = name
    node['weight'] = int(weight)
    node['children'].extend(children)


def rec_weight(node):
    """Recursively calculate the weight for all programs in this node."""
    if not node:
        return 0

    return node['weight'] + sum(rec_weight(nodes[child]) for child in node['children'])


unbalanced_nodes = []
for name, node in nodes.items():
    children = node['children']
    if children:
        counter = Counter(rec_weight(nodes[child]) for child in children)
        if len(counter) > 1:  # The recursive weigts of these children differ
            (mode, _), *_ = counter.most_common()
            black_sheep = next(child for child in children if rec_weight(nodes[child]) != mode)
            unbalanced_nodes.append(black_sheep)

for unbalanced_node in unbalanced_nodes:
    if len(set(rec_weight(nodes[child]) for child in nodes[unbalanced_node]['children'])) == 1:
        """The unbalanced node with all children in balance is the culprit."""
        parent = next(node for node in nodes.values() if unbalanced_node in node['children'])
        counter = Counter(rec_weight(nodes[child]) for child in parent['children'])
        (mode, _), (wrong, _), *_ = counter.most_common()
        diff = wrong - mode
        target_weight = nodes[unbalanced_node]['weight'] - diff
        print(target_weight)
        break
