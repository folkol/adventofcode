"""Calculates the checksum of tabular data á la https://adventofcode.com/2017/day/2."""
import fileinput


def quotient(line):
    """Returns the quotient of the first pair of numbers from `line` that divide evenly."""
    for i, x in enumerate(line):
        for j, y in enumerate(line):
            if i != j and x // y == x / y:
                return x // y
    raise Exception("Couldn't find a quotient ")


lines = ([int(x) for x in line.split()] for line in fileinput.input())
results = (quotient(line) for line in lines)

print(sum(results))
