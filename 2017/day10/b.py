from functools import reduce
from operator import xor


def rotate(lst, i):
    """Rotates the list lst i steps to the left."""
    lst[:] = lst[i:] + lst[:i]


s = '106,16,254,226,55,2,1,166,177,247,93,0,255,228,60,36'
lengths = [ord(x) for x in s] + [17, 31, 73, 47, 23]

xs = list(range(256))
pos = 0
skip = 0
for r in range(64):
    for length in lengths:
        rotate(xs, pos)
        xs[:length] = reversed(xs[:length])
        rotate(xs, -pos)
        pos = (pos + length + skip) % len(xs)
        skip += 1


def chunk(lst, i, size=16):
    """Extracts chunk #i from the given list."""
    return lst[i * size:i * size + size]


dense_hash = (reduce(xor, chunk(xs, x)) for x in range(16))
print(''.join(f'{x:02x}' for x in dense_hash))
