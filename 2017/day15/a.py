from itertools import islice

N = 40_000_000
MASK = (1 << 17) - 1  # 16 LSBs


def generator(factor, modulus=2147483647, seed=0):
    while True:
        seed = seed * factor % modulus
        yield seed


a = generator(factor=16807, seed=634)
b = generator(factor=48271, seed=301)

a = generator(factor=16807, seed=65)
b = generator(factor=48271, seed=8921)

pairs = islice(zip(a, b), N)

print(sum(1 for x, y in pairs if x & MASK == y & MASK))
