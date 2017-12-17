steps = 354

buffer = [0]
pos = 0
for n in range(2017):
    pos = ((pos + steps) % len(buffer)) + 1
    buffer.insert(pos, n + 1)

print(buffer[pos + 1])
