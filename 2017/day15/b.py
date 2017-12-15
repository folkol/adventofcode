from itertools import islice

N = 5_000_000
MASK = (1 << 16) - 1  # 16 LSBs


def generator(factor, seed, criteria, modulus=2147483647):
    while True:
        seed = seed * factor % modulus
        if seed % criteria == 0:
            yield seed


a = generator(factor=16807, seed=634, criteria=4)
b = generator(factor=48271, seed=301, criteria=8)

pairs = islice(zip(a, b), N)

print(sum(1 for x, y in pairs if x & MASK == y & MASK))
