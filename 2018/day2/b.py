import fileinput
from itertools import combinations


def find_boxes(box_ids):
    for a, b in combinations(box_ids, r=2):
        distance = sum(i != j for i, j in zip(a, b))
        if distance == 1:
            return ''.join(i for i, j in zip(a, b) if i == j)


print(find_boxes(fileinput.input()))
