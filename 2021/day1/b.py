import sys
from itertools import islice, tee

depths = (int(line) for line in sys.stdin)


def windows(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


prev, curr = tee(sum(window) for window in windows(depths, 3))
next(curr)
print(sum(1 for i, j in zip(prev, curr) if j > i))
