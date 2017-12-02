"""Calculates spreadsheep checksum á la https://adventofcode.com/2017/day/2."""
import fileinput
from itertools import permutations


def quotient(line):
    """Returns the quotient of the first pair of numbers that divide evenly."""
    return next(x // y for x, y in permutations(line, 2) if x / y == x // y)


lines = ([int(x) for x in line.split()] for line in fileinput.input())
results = (quotient(line) for line in lines)

print(sum(results))
