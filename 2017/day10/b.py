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
        dense_hash = [reduce(xor, xs[x * 16:x * 16 + 16]) for x in range(16)]
        print((16 * '{:02x}').format(*dense_hash))

chunk1 = xs[0:16]
print(chunk1[0] ^ chunk1[1] ^ chunk1[2] ^ chunk1[3] ^ chunk1[4] ^ chunk1[5] ^ chunk1[6] ^ chunk1[7] ^ chunk1[8] ^ chunk1[9] ^ chunk1[10] ^ chunk1[11] ^ chunk1[12] ^ chunk1[13] ^ chunk1[14] ^ chunk1[15])
print(reduce(xor, chunk1))

dense_hash = [reduce(xor, xs[x * 16:x * 16 + 16]) for x in range(16)]
print((16 * '{:02x}').format(*dense_hash))
