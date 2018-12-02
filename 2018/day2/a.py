import fileinput
from collections import Counter


def checksum(ids):
    twos = 0
    threes = 0
    for id in ids:
        letters = Counter(id)
        if 2 in letters.values():
            twos += 1
        if 3 in letters.values():
            threes += 1
    return twos * threes


print(checksum(fileinput.input()))
