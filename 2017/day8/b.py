from collections import defaultdict
from math import inf
from operator import ge, lt, eq, gt, le, ne
from sys import stdin

relational_operators = {
    '>=': ge,
    '<': lt,
    '==': eq,
    '>': gt,
    '<=': le,
    '!=': ne
}

highest_value = -inf
registers = defaultdict(int)
for instruction in stdin:
    reg, op, val, _, cond_reg, rel, cond_val = instruction.split()
    if relational_operators[rel](registers[cond_reg], int(cond_val)):
        if op == 'inc':
            registers[reg] += int(val)
        else:
            registers[reg] -= int(val)
    highest_value = max(registers[reg], highest_value)

print(highest_value)
