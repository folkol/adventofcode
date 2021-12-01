import sys
from collections import deque
from itertools import tee

depths = [int(line) for line in sys.stdin]


def windows(seq, n=3):
    window = deque(seq[:n - 1], maxlen=n)
    for item in seq[n - 1:]:
        window.append(item)
        yield tuple(window)


prev, curr = tee(sum(window) for window in windows(depths))
next(curr)
print(sum(1 for i, j in zip(prev, curr) if j > i))
