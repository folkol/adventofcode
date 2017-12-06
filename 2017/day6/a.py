from itertools import count
from sys import stdin

banks = [int(x) for x in stdin.read().split()]


def realloc():
    """Reallocates blocks according to https://adventofcode.com/2017/day/6."""
    i_max = banks.index(max(banks))
    num_blocks = banks[i_max]
    banks[i_max] = 0
    for _ in range(num_blocks):
        i_max = (i_max + 1) % len(banks)
        banks[i_max] += 1


seen = set()
for c in count():
    snapshot = tuple(banks)
    if snapshot in seen:
        print(c)
        break
    seen.add(snapshot)
    realloc()
