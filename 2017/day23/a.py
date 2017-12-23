def to_val(i):
    try:
        return int(i)
    except ValueError:
        return registers[i]


def op_set(reg, op):
    registers[reg] = to_val(op)


def op_sub(reg, op):
    registers[reg] -= to_val(op)


ops = {
    'set': op_set,
    'sub': op_sub,
}
program = [x.split() for x in open('program.dat')]

pc = 0
registers = {
    'a': 0,
    'b': 0,
    'c': 0,
    'd': 0,
    'e': 0,
    'f': 0,
    'g': 0,
    'h': 0
}
num_muls = 0
while 0 <= pc < len(program):
    op, *args = program[pc]

    if op == 'jnz':
        reg, arg = args
        if to_val(reg) != 0:
            pc += int(arg)
            continue
    elif op == 'mul':
        reg, arg = args
        registers[reg] *= to_val(arg)
        num_muls += 1
    else:
        ops[op](*args)

    pc += 1
    # print(pc, registers)

print(num_muls)