"""Calculates spreadsheep checksum á la https://adventofcode.com/2017/day/2."""
import fileinput
from itertools import permutations


def even_quotient(line):
    """Returns the quotient of the first pair of numbers that divide evenly."""
    return next(x // y for x, y in permutations(line, 2) if (x / y).is_integer())


rows = ([int(x) for x in line.split()] for line in fileinput.input())

print(sum(even_quotient(row) for row in rows))
