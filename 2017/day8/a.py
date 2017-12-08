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

registers = defaultdict(int)
for instruction in open('instructions.dat'):
    reg1, op, val, _, reg2, rel, immediate = re.findall('\S+', instruction)
    if relational_operators[rel](registers[reg2], int(immediate)):
        if op == 'inc':
            registers[reg1] += int(val)
        else:
            registers[reg1] -= int(val)

print(max(registers.values()))
