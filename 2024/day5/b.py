from collections import defaultdict
from functools import cmp_to_key


def comparator(a, b):
    if a in sort_order[b]:
        return -1
    elif b in sort_order[a]:
        return 1
    else:
        return 0


sort_order = defaultdict(list)
with open("input.dat") as f:
    while (line := f.readline()) != "\n":
        a, b = line.split("|")
        sort_order[int(b)].append(int(a))

    updates = [[int(p) for p in page.rstrip().split(",")] for page in f]

ans = sum(
    in_order[len(in_order) // 2]
    for (original, in_order)
    in [(u, sorted(u, key=cmp_to_key(comparator))) for u in updates]
    if original != in_order
)

print(ans)
