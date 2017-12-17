steps = 354

buffer = [0]
pos = 0
for n in range(2017):
    pos = (pos + steps) % len(buffer)
    buffer.insert(pos + 1, n + 1)
    pos += 1

print(buffer[pos + 1])
