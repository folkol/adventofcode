from itertools import count
from sys import stdin

maze = [int(x) for x in stdin.readlines()]

pc = 0
try:
    for i in count():
        delta = maze[pc]
        if delta > 2:
            maze[pc] -= 1
        else:
            maze[pc] += 1
        pc += delta
except IndexError:
    pass

print(f'i: {i}')
