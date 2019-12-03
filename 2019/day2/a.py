from functools import partial

with open('input.dat') as f:
    data = f.read()
    program = list(map(int, data.split(',')))

OP_ADD = 1
OP_MUL = 2
OP_HLT = 99

program[1], program[2] = 12, 2  # Restoring 1202 state

PC = 0
while True:
    op_code = program[PC]
    if op_code == OP_ADD:
        a, b, c = program[PC + 1: PC + 4]
        program[c] = program[a] + program[b]
    elif op_code == OP_MUL:
        a, b, c = program[PC + 1: PC + 4]
        program[c] = program[a] * program[b]
    elif op_code == OP_HLT:
        break
    else:
        print(f'Unknown op_code: {op_code}')
    PC += 4

print(program[0])  # 9706670