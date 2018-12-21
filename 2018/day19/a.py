import re


def addr(regs, A, B, C):
    regs[C] = regs[A] + regs[B]


def addi(regs, A, B, C):
    regs[C] = regs[A] + B


def mulr(regs, A, B, C):
    regs[C] = regs[A] * regs[B]


def muli(regs, A, B, C):
    regs[C] = regs[A] * B


def banr(regs, A, B, C):
    regs[C] = regs[A] & regs[B]


def bani(regs, A, B, C):
    regs[C] = regs[A] & B


def borr(regs, A, B, C):
    regs[C] = regs[A] | regs[B]


def bori(regs, A, B, C):
    regs[C] = regs[A] | B


def setr(regs, A, _, C):
    regs[C] = regs[A]


def seti(regs, A, B, C):
    regs[C] = A


def gtir(regs, A, B, C):
    regs[C] = A > regs[B]


def gtri(regs, A, B, C):
    regs[C] = regs[A] > B


def gtrr(regs, A, B, C):
    regs[C] = regs[A] > regs[B]


def eqir(regs, A, B, C):
    regs[C] = A == regs[B]


def eqri(regs, A, B, C):
    regs[C] = regs[A] == B


def eqrr(regs, A, B, C):
    regs[C] = regs[A] == regs[B]


with open('prog.dat') as f:
    registers = [0, 0, 0, 0, 0, 0]
    ipr = int(next(f).split()[1])
    program = [re.match(r'(\w+) (\d+) (\d+) (\d+)', line).groups() for line in f]

IP = 0
while True:
    if IP < 0 or IP >= len(program):
        break
    op, A, B, C = program[IP]
    pre = registers.copy()
    registers[ipr] = IP
    locals()[op](registers, int(A), int(B), int(C))
    IP = registers[ipr]
    # print(IP, op, A, B, C, *pre, '->', *registers, sep='\t')
    IP += 1

print(registers[0], sep='\t')
