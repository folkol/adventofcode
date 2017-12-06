from itertools import count

banks = [int(x) for x in '11	11	13	7	0	15	5	5	4	4	1	1	7	1	15	11'.split()]

seen = set()

for c in count():
    # print(seen)
    if tuple(banks) in seen:
        break
    seen.add(tuple(banks))
    i = banks.index(max(banks))
    num_blocks = banks[i]
    banks[i] = 0
    for _ in range(num_blocks):
        i = (i + 1) % len(banks)
        banks[i] += 1

print(c)
