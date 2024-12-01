with open("input.dat") as f:
    data = [[int(x) for x in line.split()] for line in f]

lefts, rights = (sorted(xs) for xs in zip(*data))
distances = (abs(left - right) for left, right in zip(lefts, rights))

print(sum(distances))
