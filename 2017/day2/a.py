"""Calculates spreadsheet checksum á la https://adventofcode.com/2017/day/2."""
import fileinput

rows = ([int(x) for x in line.split()] for line in fileinput.input())
ranges = (max(line) - min(line) for line in rows)

print(sum(ranges))
