import re
from collections import defaultdict
from operator import ge, lt, eq, gt, le, ne

relational_operators = {
    '>=': ge,
    '<': lt,
    '==': eq,
    '>': gt,
    '<=': le,
    '!=': ne
}

highest_value = float('-inf')
registers = defaultdict(int)
for instruction in open('instructions.dat'):
    reg, op, val, _, cond_reg, rel, cond_val = re.findall('\S+', instruction)
    if relational_operators[rel](registers[cond_reg], int(cond_val)):
        if op == 'inc':
            registers[reg] += int(val)
        else:
            registers[reg] -= int(val)
    highest_value = max(registers[reg], highest_value)

print(highest_value)
