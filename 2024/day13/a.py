import re
from functools import cache
from itertools import batched

import math

with open('input.dat') as f:
    numbers = (int(x) for x in re.findall(r'\d+', f.read()))


@cache
def min_tokens(a_x, a_y, b_x, b_y, target_x, target_y, pos_x, pos_y, tokens):
    if pos_x > target_x or pos_y > target_y:
        return math.inf

    if pos_x == target_x and pos_y == target_y:
        return tokens

    return min(
        min_tokens(a_x, a_y, b_x, b_y, target_x, target_y, pos_x + a_x, pos_y + a_y, tokens + 3),
        min_tokens(a_x, a_y, b_x, b_y, target_x, target_y, pos_x + b_x, pos_y + b_y, tokens + 1),
    )


tokens = (min_tokens(*machine, 0, 0, 0) for machine in batched(numbers, 6))
print(sum(token for token in tokens if token < math.inf))
