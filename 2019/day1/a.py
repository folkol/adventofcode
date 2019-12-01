with open('input.dat') as f:
    data = [int(d.rstrip()) for d in f]

print(sum(d // 3 - 2 for d in data))
