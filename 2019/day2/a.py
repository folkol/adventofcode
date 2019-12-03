from functools import partial
import sys

with open('input.dat') as f:
    data = f.read()
    program = list(map(int, data.split(',')))

def op_add(program, a, b, c):
    program[c] = program[a] + program[b]

def op_mul(program, a, b, c):
    program[c] = program[a] * program[b]

def op_hlt(program, *_):
    print(f'program[0]: {program[0]}')  # 9706670
    sys.exit(1)


OP = {
    1: op_add,
    2: op_mul,
    99: op_hlt
}

program[1], program[2] = 12, 2  # Restoring 1202 state
PC = 0
while True:
    op_code = program[PC]
    OP[op_code](program, *program[PC + 1: PC + 4])
    PC += 4
