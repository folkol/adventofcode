import re

with open('input.dat') as f:
    numbers = [int(n) for n in (re.findall(r'\d+', f.read()))]
    A, B, C, *text = numbers


def combo(x):
    return {4: A, 5: B, 6: C}.get(x, x)


outputs = []
pc = 0
while pc < len(text):
    op, operand = text[pc:pc + 2]
    if op == 0:  # adv
        A //= 2 ** combo(operand)
    elif op == 1:  # bxl
        B ^= operand
    elif op == 2:  # bst
        B = combo(operand) % 8
    elif op == 3:  # jnz
        if A:
            pc = operand
            continue
    elif op == 4:  # bxc
        B ^= C
    elif op == 5:  # out
        outputs.append(combo(operand) % 8)
    elif op == 6:  # bdv
        B = A // 2 ** combo(operand)
    elif op == 7:  # cdv
        C = A // 2 ** combo(operand)
    pc += 2

print(*outputs, sep=',')
