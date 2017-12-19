from collections import defaultdict

program = [x.split() for x in open('program.dat')]
LATEST_SOUND = 'LATEST_SOUND'
registers = defaultdict(int)


def op_set(reg, value):
    try:
        registers[reg] = int(value)
    except ValueError:
        registers[reg] = registers[value]


def op_add(reg, value):
    registers[reg] += int(value)


def op_mul(reg, value):
    try:
        registers[reg] *= int(value)
    except ValueError:
        registers[reg] *= registers[value]


def op_mod(reg, value):
    try:
        registers[reg] %= int(value)
    except ValueError:
        registers[reg] %= registers[value]


def op_snd(reg):
    registers[LATEST_SOUND] = registers[reg]


ops = {
    'set': op_set,
    'add': op_add,
    'mul': op_mul,
    'mod': op_mod,
    'snd': op_snd
}
pc = 0
while True:
    op, *args = program[pc]

    if op == 'jgz':
        reg, arg = args
        if registers[reg] > 0:
            pc += int(arg)
            continue
    elif op == 'rcv':
        reg = args[0]
        if registers[reg]:
            registers[reg] = registers[LATEST_SOUND]
            print(registers[reg])
            break
    else:
        ops[op](*args)

    pc += 1
