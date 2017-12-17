steps = 354

buffer = [0]
pos = 0
for n in range(50_000_000):
    pos = ((pos + steps) % len(buffer)) + 1
    buffer.insert(pos, n + 1)
    print(buffer.index(0), len(buffer), buffer[buffer.index(0) + 1])

print(buffer[pos + 1])
