from operator import itemgetter

SERIAL_NO = 8979
grid = {}
for x in range(1, 301):
    for y in range(1, 301):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += SERIAL_NO
        power_level *= rack_id
        digit = format(power_level, '03d')[-3]
        power_level = int(digit)
        power_level -= 5
        grid[(x, y)] = power_level

total_power = {}
for s in range(1, 300):
    print(s)
    for x in range(1, 301 - s):
        for y in range(1, 301 - s):
            previous = total_power.get((x, y, s - 1), 0)
            total_power[(x, y, s)] = \
                previous + \
                sum(grid[(x + i, y + s - 1)] for i in range(s - 1)) + \
                sum(grid[(x + s - 1, y + j)] for j in range(s - 1)) + \
                grid[(x + s - 1, y + s - 1)]

print(max(total_power.items(), key=itemgetter(1)))
