with open('input.dat') as f:
    data = [int(d.rstrip()) for d in f]

fuel = 0
for d in data:
    d = d // 3 - 2
    while d > 0:
        fuel += d
        d = d // 3 - 2

print(fuel)