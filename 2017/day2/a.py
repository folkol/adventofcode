"""Calculates the checksum of tabular data á la https://adventofcode.com/2017/day/2."""
import fileinput

lines = ([int(x) for x in line.split()] for line in fileinput.input())
diff = (max(line) - min(line) for line in lines)

print(sum(diff))
