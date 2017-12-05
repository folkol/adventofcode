from itertools import count
from sys import stdin

maze = [int(x) for x in stdin.readlines()]

pc = 0
try:
    for i in count():
        maze[pc], pc = maze[pc] + 1, pc + maze[pc]
except IndexError:
    pass

print(f'i: {i}')
