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

sequences = defaultdict(int)
for seed in seeds:
    changes = deque(islice(rng(seed), 4), maxlen=4)
    seen = set()
    for a, b in pairwise(rng(seed)):
        changes.append(b - a)
        sequence = tuple(changes)
        if sequence not in seen:
            sequences[sequence] += a
            seen.add(sequence)

print(max(sequences.values()))
