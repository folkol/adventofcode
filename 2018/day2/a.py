import fileinput
from collections import Counter


def checksum(box_ids):
    twos = 0
    threes = 0
    for box_id in box_ids:
        letters = Counter(box_id)
        if 2 in letters.values():
            twos += 1
        if 3 in letters.values():
            threes += 1
    return twos * threes


print(checksum(fileinput.input()))
