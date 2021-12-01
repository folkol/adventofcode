import sys
from itertools import tee

prev, curr = tee(int(line) for line in sys.stdin)
next(curr)
print(sum(1 for i, j in zip(prev, curr) if j > i))
