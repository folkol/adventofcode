from collections import Counter

with open("input.dat") as f:
    data = [[int(x) for x in line.split()] for line in f]

lefts, rights = zip(*data)
right_counts = Counter(rights)
print(sum(left * right_counts[left] for left in lefts))
