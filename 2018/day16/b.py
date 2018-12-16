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


def behaves_like(ops, before, instruction, after):
    result = []
    for op in ops:
        n, A, B, C = instruction
        regs = list(before)
        op(regs, A, B, C)
        if regs == list(after):
            result.append(op)
    return result


ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
instruction_set = {}
behaves = defaultdict(set)
for before, instruction, after in samples:
    candidates = behaves_like(ops, before, instruction, after)
    for candidate in candidates:
        behaves[instruction[0]].add(candidate)

while behaves:
    for op, candidates in list(behaves.items()):
        if len(candidates) == 1:
            candidate = candidates.pop()
            instruction_set[op] = candidate
            for k, v in behaves.items():
                if candidate in v:
                    v.remove(candidate)
            del behaves[op]

for i, op in sorted(instruction_set.items()):
    print(i, op.__name__)

with open('prog.dat') as f:
    registers = [0, 0, 0, 0]
    for line in f:
        op, A, B, C = [int(g) for g in re.findall(r'\d+', line)]
        instruction_set[op](registers, A, B, C)
        print(f'{instruction_set[op].__name__.upper()} {A} {B} {C} |', *(int(r) for r in registers))

print(registers[0], sep='\t')
