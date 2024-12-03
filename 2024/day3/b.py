import re

PATTERN = r"mul\((\d+),(\d+)\)|(do)\(\)|(don't)\(\)"

with open('input.dat') as f:
    instructions = re.findall(PATTERN, f.read())

active = True
answer = 0

for instructions in instructions:
    match instructions:
        case [a, b, '', ''] if active:
            answer += int(a) * int(b)
        case ['', '', 'do', _]:
            active = True
        case ['', '', _, "don't"]:
            active = False

print(answer)
