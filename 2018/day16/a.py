import re
from pprint import pprint

with open('samples.dat') as f:
    samples = []
    for line in f:
        m = re.match(r'Before: \[(\d+), (\d+), (\d+), (\d+)\]', line)
        if m:
            before = tuple(int(g) for g in m.groups())
        m = re.match(r'(\d+) (\d+) (\d+) (\d+)', line)
        if m:
            instruction = tuple(int(g) for g in m.groups())
        m = re.match(r'After:  \[(\d+), (\d+), (\d+), (\d+)\]', line)
        if m:
            after = tuple(int(g) for g in m.groups())
            samples.append((before, instruction, after))

pprint(samples)


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


def behaves_like(before, instruction, after):
    ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
    num_like = 0
    for op in ops:
        _, A, B, C = instruction
        regs = list(before)
        op(regs, A, B, C)
        if regs == list(after):
            num_like += 1
    return num_like


print(sum(behaves_like(*sample) >= 3 for sample in samples))
