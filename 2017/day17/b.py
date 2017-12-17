steps = 354

pos = 0
buffer_len = 1
after_zero = None
for n in range(50_000_000):
    pos = ((pos + steps) % buffer_len) + 1
    if pos == 1:
        after_zero = n + 1
    buffer_len += 1

print(after_zero)
