import fileinput
from itertools import combinations
from typing import Sequence


def find_similar(box_ids: Sequence[str]):
    for a, b in combinations(box_ids, r=2):
        distance = sum(i != j for i, j in zip(a, b))
        if distance == 1:
            return ''.join(i for i, j in zip(a, b) if i == j)


print(find_similar(fileinput.input()))
