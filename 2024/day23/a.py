from collections import defaultdict
from itertools import combinations

with open('input.dat') as f:
    network = defaultdict(set)
    for line in f:
        a, b = line.strip().split('-')
        network[a].add(b)
        network[b].add(a)


def valid_triple(i, j, k):
    interconnected = i in network[j] and i in network[k] and j in network[k]
    return interconnected and any(c.startswith('t') for c in [i, j, k])


triples = [
    triple
    for triple in combinations(network, 3)
    if valid_triple(*triple)
]
print(len(triples))
