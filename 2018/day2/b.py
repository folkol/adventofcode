import fileinput
from itertools import combinations
from typing import Sequence


def common_letters(a, b):
    return ''.join(i for i, j in zip(a, b) if i == j)


def find_similar(box_ids: Sequence[str]):
    for a, b in combinations(box_ids, r=2):
        distance = sum(i != j for i, j in zip(a, b))
        if distance == 1:
            return common_letters(a, b)


print(find_similar(fileinput.input()))
