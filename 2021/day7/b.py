def distance(n, x):
    p = abs(n - x)
    return p * (p + 1) // 2


with open('input.dat') as f:
    data = [int(n) for n in f.read().split(',')]

prev = float('inf')
for n in range(min(data), max(data) + 1):
    cost = sum(distance(n, x) for x in data)
    if cost > prev:
        print(prev)
        break
    prev = cost
