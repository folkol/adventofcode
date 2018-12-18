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


for minute in range(10):
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
    acres = new_acres
    plot()
print(acres)
l = list(acres.values())
print(l)
print(l.count('|') * l.count('#'))
