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
for x in range(1, 301 - 2):
    for y in range(1, 301 - 2):
        total_power[(x, y)] = sum(grid[(x + i, y + j)] for i in range(3) for j in range(3))

print(max(total_power.items(), key=itemgetter(1)))
