with open('input.dat') as f:
    reports = [[int(x) for x in line.split()] for line in f]


def pairs(xs):
    return zip(xs, xs[1:])


def is_strictly_monotonic(xs):
    return all(a < b for a, b in pairs(xs)) or all(a > b for a, b in pairs(xs))


def slope(xs):
    return [b - a for b, a in pairs(xs)]


def is_safe(xs):
    return is_strictly_monotonic(xs) and all(abs(k) <= 3 for k in slope(xs))


print(sum(is_safe(r) for r in reports))
