from functools import reduce
from statistics import median

LBRACKETS, RBRACKETS = '([{<', ')]}>'
COMPLEMENT = {k: v for k, v in zip(LBRACKETS + RBRACKETS, RBRACKETS + LBRACKETS)}
VALUES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def autocomplete(line):
    stack = []
    for i, c in enumerate(line):
        if c in LBRACKETS:
            stack.append(c)
        elif stack[-1] == COMPLEMENT[c]:
            stack.pop()
        else:
            return

    return [COMPLEMENT[c] for c in reversed(stack)]


with open('input.dat') as f:
    lines = f.read().splitlines()
    scores = []
    for line in lines:
        if suffix := autocomplete(line):
            score = reduce(lambda acc, c: acc * 5 + VALUES[c], suffix, 0)
            scores.append(score)

print(median(scores))
