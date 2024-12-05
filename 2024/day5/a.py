from collections import defaultdict
from functools import cmp_to_key


def comparator(a, b):
    if a in order[b]:
        return -1
    elif b in order[a]:
        return 1
    else:
        return 0


order = defaultdict(list)
with open("input.dat") as f:
    while (line := f.readline()) != '\n':
        a, b = line.split('|')
        order[int(b)].append(int(a))

    updates = [[int(p) for p in page.rstrip().split(',')] for page in f]

updates_in_order = (u for u in updates if u == sorted(u, key=cmp_to_key(comparator)))
print(sum(u[len(u) // 2] for u in updates_in_order))
