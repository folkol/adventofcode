import re
from itertools import batched

with open('input.dat') as f:
    numbers = (int(x) for x in re.findall(r'\d+', f.read()))


def solve(ax, ay, bx, by, x, y):
    """Solve linear system, return 0 solution is not integer."""
    determinant = ax * by - bx * ay
    a = (by * x - bx * y) // determinant
    b = (ax * y - x * ay) // determinant

    if a * ax + b * bx == x and a * ay + b * by == y:
        return 3 * a + 1 * b
    return 0


print(sum(
    solve(*params, x + 10000000000000, y + 10000000000000)
    for *params, x, y
    in batched(numbers, 6)
))
