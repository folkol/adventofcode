with open('input.dat') as f:
    schematics = f.read().split('\n\n')

locks, keys = [], []
for schematic in schematics:
    lines = schematic.splitlines()
    column_heights = [column.count('#') - 1 for column in list(zip(*lines))]
    if lines[0] == '#####':
        locks.append(column_heights)
    else:
        keys.append(column_heights)


def fits(key, lock):
    return all(a + b <= 5 for a, b in zip(key, lock))


print(sum(fits(key, lock) for key in keys for lock in locks))
