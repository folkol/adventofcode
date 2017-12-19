from collections import defaultdict

LATEST_SOUND = 'LATEST_SOUND'

source_code = '''set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2'''

program = [x.split() for x in open('program.dat')]

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
    op, reg, *args = program[pc]

    if op == 'jgz':
        if registers[reg] > 0:
            pc += int(args[0])
            continue
    elif op == 'rcv':
        if registers[reg]:
            registers[reg] = registers[LATEST_SOUND]
            print(registers[reg])
            break
    else:
        ops[op](reg, *args)

    pc += 1
