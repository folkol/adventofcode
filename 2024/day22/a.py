from functools import reduce

with open('input.dat') as f:
    seeds = [int(seed) for seed in f]


def rng(seed):
    seed ^= seed * 64 % 16777216
    seed ^= seed // 32 % 16777216
    seed ^= seed * 2048 % 16777216
    return seed


print(sum(reduce(lambda s, _: rng(s), range(2000), seed) for seed in seeds))
