import re
from collections import defaultdict

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


def find_candidates(before, instruction, after):
    candidates = []
    for op in [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]:
        _, A, B, C = instruction
        regs = list(before)
        op(regs, A, B, C)
        if regs == list(after):
            candidates.append(op)
    return candidates


ops = {}
candidates = defaultdict(set)
for before, instruction, after in samples:
    for candidate in find_candidates(before, instruction, after):
        op, *_ = instruction
        candidates[op].add(candidate)

while candidates:
    for op, candidate in [(op, functions.pop()) for op, functions in candidates.items() if len(functions) == 1]:
        for functions in candidates.values():
            if candidate in functions:
                functions.remove(candidate)
        del candidates[op]
        ops[op] = candidate

with open('prog.dat') as f:
    registers = [0, 0, 0, 0]
    for line in f:
        op, A, B, C = [int(g) for g in re.findall(r'\d+', line)]
        ops[op](registers, A, B, C)

assert registers[0] == 537, registers[0]
print(registers[0], sep='\t')
