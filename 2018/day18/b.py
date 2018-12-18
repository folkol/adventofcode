with open('map.dat') as f:
    acres = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            acres[(x, y)] = c

x_max = max(x for x, y in acres)
y_max = max(y for x, y in acres)


def plot():
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            acre = acres[(x, y)]
            print(acre, end='')
        print()
    print()


def generation(acres):
    new_acres = acres.copy()
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            acre = acres[(x, y)]
            adjacent = [acres.get((x + dx, y + dy)) for dy in range(-1, 2) for dx in range(-1, 2) if (dx, dy) != (0, 0)]

            if acre == '.':
                if adjacent.count('|') >= 3:
                    new_acres[(x, y)] = '|'
            elif acre == '|':
                if adjacent.count('#') >= 3:
                    new_acres[(x, y)] = '#'
            elif acre == '#':
                if adjacent.count('#') >= 1 and adjacent.count('|') >= 1:
                    new_acres[(x, y)] = '#'
                else:
                    new_acres[(x, y)] = '.'
            else:
                raise Exception('wuut: ' + acre)
    return new_acres


N = 1000000000
n = 0
initial = acres.copy()
seen = []
while n < N:
    acres = generation(acres)
    if acres in seen:
        i = seen.index(acres)
        cycle_length = n - i
        print('Cycle at', n, cycle_length)
        while n < N - cycle_length:
            n += cycle_length
        seen.clear()
    seen.append(acres)
    # if acres == initial:
    #     print('Repeats at n', n)
    #     break
    print(n)
    n += 1
    # plot()
cells = list(acres.values())
print(cells.count('|') * cells.count('#'))
