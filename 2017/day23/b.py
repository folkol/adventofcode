"""Hand-optimized version:

    b = 109300
    c = 126300

    for(int i = b; b < c; b += 17) {
        f = 1
        for(int d = 2; d < b; d++) {
            for(int e = 2; e < b; e++) {
                if(d * e == b) { // Found factorization of b
                    f = 0
                }
            }
        }
        if(f == 0) {
            h++
        }
    }

    print(h)

    Essentially: Counting non-prime numbers in the range 126300–109300


    def is_prime(a):
        return all(a % i for i in range(2, a))


    b = 109300
    c = 126300
    h = 0

    for b in range(109300, 126300 + 1, 17):
        if not is_prime(b):
            h += 1

    print(h)
"""


def to_val(i):
    try:
        return int(i)
    except ValueError:
        return registers[i]


def op_set(reg, op):
    registers[reg] = to_val(op)


def op_sub(reg, op):
    registers[reg] -= to_val(op)


def op_mul(reg, op):
    registers[reg] *= to_val(op)


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
while 0 <= pc < len(program):
    op, *args = program[pc]

    if op == 'jnz':
        reg, arg, *_ = args
        if to_val(reg) != 0:
            pc += int(arg)
            continue
    else:
        ops[op](*args)

    pc += 1

print(registers['h'])
