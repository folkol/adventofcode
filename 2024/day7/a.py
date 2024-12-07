import re


def any_combo(target, operands, x=None):
    if not operands:
        return x == target
    first, *rest = operands
    return any_combo(target, rest, (x or 0) + first) or any_combo(target, rest, (x or 0) * first)


with open('input.dat') as f:
    equations = [[int(x) for x in re.findall(r'\d+', line)] for line in f]

print(sum((v for v, *numbers in equations if any_combo(v, numbers))))
