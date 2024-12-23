from collections import defaultdict

with open('input.dat') as f:
    network = defaultdict(set)
    for a, b in (line.rstrip().split('-') for line in f):
        network[a].add(b)
        network[b].add(a)


def bron_kerbosch(r, p, x, acc):
    if not p and not x:
        acc.append(sorted(r))
    for v in list(p):
        bron_kerbosch(r | {v}, p & network[v], x & network[v], acc)
        p = p - {v}
        x = x & {v}


maximal_cliques = []
bron_kerbosch(set(), set(network), set(), maximal_cliques)
print(','.join(max(maximal_cliques, key=len)))
