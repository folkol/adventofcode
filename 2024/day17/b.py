import re

with open('input.dat') as f:
    numbers = [int(n) for n in (re.findall(r'\d+', f.read()))]
    text = numbers[3:]


def run(A, B, C):
    outputs = []
    pc = 0
    while pc < len(text):
        op, operand = text[pc:pc + 2]
        combo = [0, 1, 2, 3, A, B, C][operand]
        if op == 0:  # adv
            A //= 2 ** combo
        elif op == 1:  # bxl
            B ^= operand
        elif op == 2:  # bst
            B = combo % 8
        elif op == 3:  # jnz
            if A:
                pc = operand
                continue
        elif op == 4:  # bxc
            B ^= C
        elif op == 5:  # out
            outputs.append(combo % 8)
        elif op == 6:  # bdv
            B = A // 2 ** combo
        elif op == 7:  # cdv
            C = A // 2 ** combo
        pc += 2
    return outputs


def find_seed(seed, i):
    """Search for valid A, one octal digit at the time.

    - The program seems to calculate one `output` per iteration
    - The only loop-carried dependency is A
    - The `output` is "some expression of the (octal) LSB of A"
    - A is shifted 3 bits per iteration

    We can brute-force one digit at the time and recurse.
    """
    for lsd in range(8):
        candidate = seed * 8 + lsd
        if run(candidate, 0, 0) == text[i:]:
            if i == 0:
                return candidate
            if ans := find_seed(candidate, i - 1):
                return ans


print(find_seed(0, len(text) - 1))
