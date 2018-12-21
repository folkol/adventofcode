"""
#ip 1
00: seti 123 0 4        ; #4 = 123              ; #4 = 123
01: bani 4 456 4        ; #4 = #4 & 456         ; #4 = 72
02: eqri 4 72 4         ; #4 = #4 == 72         ; #4 = 1
03: addr 4 1 1          ; #1 = #1 + #4          ; GOTO 05
04: seti 0 0 1          ; #1 = 0                ; GOTO 0
05: seti 0 1 4          ; #4 = 0                ; #4 = 0
06: bori 4 65536 3      ; #3 = #4 | 65536       ; #3 = #4 | 65536
07: seti 3730679 4 4    ; #4 = 3730679          ; #4 = 3730679
08: bani 3 255 5        ; #5 = #3 & 255         ; #5 = #3 & 255
09: addr 4 5 4          ; #4 = #4 + #5          ; #4 += #5
10: bani 4 16777215 4   ; #4 = #4 & 16777215    ; mask out 24 bits
11: muli 4 65899 4      ; #4 = #4 * 65899       ; #4 *= 65899
12: bani 4 16777215 4   ; #4 = #4 & 16777215    ; mask out 24 bits
13: gtir 256 3 5        ; #5 = 256 > #3         ; if 256 > #3:
14: addr 5 1 1          ; #1 = #1 + #5          ;   GOTO 16
15: addi 1 1 1          ; #1 = #1 + 1           ; GOTO 17
16: seti 27 1 1         ; #1 = 27               ; GOTO 28
17: seti 0 0 5          ; #5 = 0                ; #5 = 0
18: addi 5 1 2          ; #2 = #5 + 1           ; #2 = #5 + 1
19: muli 2 256 2        ; #2 = #2 * 256         ; #2 *= 256
20: gtrr 2 3 2          ; #2 = #2 > #3          ; if #2 > #3:
21: addr 2 1 1          ; #1 = #2 + #1          ;   GOTO 23
22: addi 1 1 1          ; #1 = #1 + 1           ; GOTO 24
23: seti 25 1 1         ; #1 = 25               ; GOTO 26
24: addi 5 1 5          ; #5 = #5 + 1           ; #5 += 1
25: seti 17 1 1         ; #1 = 17               ; GOTO 18
26: setr 5 2 3          ; #3 = #5               ; #3 = #5
27: seti 7 6 1          ; #1 = 7                ; GOTO 8
28: eqrr 4 0 5          ; #5 = #4 > #0          ; if #4 > #0:
29: addr 5 1 1          ; #1 = #1 + #5          ;   HALT
30: seti 5 1 1          ; #1 = 5                ; GOTO 6
"""

# 05: r4 = 0
# 06: ...
# 07: r4 = 3730679
# 08: #5 = #3 & 255
# 09: r4 += #5
# 10: mask out 24 bits
# 11: r4 *= 65899
# 12: mask out 24 bits
# 13: if 256 > #3:
# 14:   GOTO 16
# 15: GOTO 17
# 16: GOTO 28
# 17: #5 = 0
# 18: #2 = #5 + 1
# 19: #2 *= 256
# 20: if #2 > #3:
# 21:   GOTO 23
# 22: GOTO 24
# 23: GOTO 26
# 24: #5 += 1
# 25: GOTO 18
# 26: #3 = #5
# 27: GOTO 8
# 28: if r4 > #0:
# 29:   HALT
# 30: GOTO 6


#     while True:
# 07:     r4 = 3730679
#         while True:
# 08:         #5 = #3 & 255
# 09:         r4 += #5
# 10:         mask out 24 bits out of #4
# 11:         r4 *= 65899
# 12:         mask out 24 bits out of #4
# 13:         if 256 > #3 and r4 == #0:
#                 HALT
# 17:         #5 = 0
#             while True:
# 18:             #2 = #5 + 1
# 19:             #2 *= 256
# 20:             if #2 > #3:
#                     GOTO 26
# 24:             #5 += 1
# 26:         #3 = #5


#     while True:
# 07:     r4 = 3730679
#         while True:
# 08:         #5 = 256
# 09:         r4 += #5
# 10:         mask out 24 bits out of #4
# 11:         r4 *= 65899
# 12:         mask out 24 bits out of #4
# 13:         if 256 > #3 and r4 == #0:
#                 HALT
# 17:         #5 = 63257
#
# 18:
# 19:
# 20:
#
# 24:
# 26:         #3 = 63257

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

# First time we get to IP 28, r4 is 16128384
m = IP = 0
seen = set()
while True:
    if IP < 0 or IP >= len(program):
        break
    # print()
    # for i, r in enumerate(registers):
    #     print(f'#{i}={r}')
    # for i, line in enumerate(program):
    #     print('> ' if i == IP else '  ', format(i, '02d'), *line)
    op, A, B, C = program[IP]
    if IP == 28:
        r4 = registers[4]
        print(len(seen), r4)
        if r4 in seen:
            # Last number before repetition is the key
            print('Repetition with r4 ==', r4)
            break
        seen.add(r4)

    registers[ipr] = IP
    locals()[op](registers, int(A), int(B), int(C))
    IP = registers[ipr]
    IP += 1
