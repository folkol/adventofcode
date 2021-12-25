import re

with open('input.dat') as f:
    match = re.match(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)', f.read())
    x1, x2, y1, y2 = [int(d) for d in match.groups()]

target_area = (int(x1), int(y2), int(x2), int(y1))
bottom_line = target_area[3]
max_dy = (bottom_line ** 2 + bottom_line) // 2


def hits_target(idx, idy):
    dx, dy, x, y = idx, idy, 0, 0
    while True:
        if dx == 0 and y > 0:
            y, dy = 0, -idy - 1
        if dx == 0 and x < x1:
            return False
        if x > x2:
            return False
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
        if x < x1 and dx < 0:
            return False
        if x > x2 and dx > 0:
            return False
        if y < y1 and dy < 0:
            return False
        x, y = x + dx, y + dy
        dy -= 1
        if dx > 0:
            dx -= 1


good_initials = sum(
    hits_target(dx, dy)
    for dx in range(target_area[2] + 1)
    for dy in range(-max_dy, max_dy + 1)
)
print(good_initials)
