with open("input.dat") as f:
    data = [[int(x) for x in line.split()] for line in f]

left, right = zip(*data)

print(sum(abs(a - b) for a, b in zip(sorted(left), sorted(right))))
