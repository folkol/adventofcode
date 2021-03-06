import fileinput
import re
from collections import defaultdict

squares = defaultdict(int)
lines = [line for line in fileinput.input()]
for line in lines:
    claim, x, y, width, height = (int(n) for n in re.findall('(\d+)', line))
    for i in range(width):
        for j in range(height):
            squares[x + i, y + j] += 1

print(sum(x > 1 for x in squares.values()))
