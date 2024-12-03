import re

with open('input.dat') as f:
    instructions = re.findall(r'mul\((\d+),(\d+)\)', f.read())

print(sum(int(a) * int(b) for a, b in instructions))
