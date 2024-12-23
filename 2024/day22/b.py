from collections import deque, defaultdict
from itertools import pairwise, islice


def rng(seed):
    for _ in range(2000):
        yield seed % 10
        seed ^= seed * 64 % 16777216
        seed ^= seed // 32 % 16777216
        seed ^= seed * 2048 % 16777216


with open("input.dat") as file:
    seeds = [int(seed) for seed in file]

sequences = defaultdict(list)
for seed in seeds:
    changes = deque(islice(rng(seed), 4), maxlen=4)
    visited = set()
    for n, m in pairwise(rng(seed)):
        changes.append(m - n)
        sequence = tuple(changes)
        if sequence not in visited:
            sequences[sequence].append(n)
            visited.add(sequence)

print(max(sum(values) for values in sequences.values()))
