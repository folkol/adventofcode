with open('input.dat') as f:
    disk_map = [
        str(block)
        for i, e in enumerate(f.read())
        for block in [i // 2 if i % 2 == 0 else '.'] * int(e)
    ]

i, j = 0, len(disk_map) - 1
while True:
    while disk_map[i] != '.':
        i += 1
    while disk_map[j] == '.':
        j -= 1
    if i > j:
        break
    disk_map[j], disk_map[i] = disk_map[i], disk_map[j]

print(sum(int(i) * int(j) if j != '.' else 0 for i, j in enumerate(disk_map)))
