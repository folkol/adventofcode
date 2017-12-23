def to_matrix(s):
    """'123/456/789' -> [[1,2,3],[4,5,6],[7,8,9]]"""
    return [list(row) for row in s.split('/')]


def to_string(m):
    """[[1,2,3],[4,5,6],[7,8,9]] -> '123/456/789'"""
    return '/'.join(''.join(x) for x in m)


def symmetries(matrix):
    """Generates the rotation and reflection symmetries of `matrix`."""

    def rotate(m):
        return list(zip(*m[::-1]))

    def vflip(m):
        return [row[::-1] for row in m]

    def hflip(m):
        return m[::-1]

    def dflip(m):
        return rotate(hflip(m))

    def dflip2(m):
        return rotate(vflip(m))

    yield matrix
    yield rotate(matrix)
    yield rotate(rotate((matrix)))
    yield rotate(rotate(rotate((matrix))))
    yield vflip(matrix)
    yield hflip(matrix)
    yield dflip(matrix)
    yield dflip2(matrix)


def expand_rules(data):
    for datum in data:
        rule, result = datum.split(' => ')
        for symmetry in symmetries(to_matrix(rule)):
            yield to_string(symmetry), result


def enhance(pattern, n, m):
    """Creates an enhanced pattern according to `rules`."""

    def mslice(m, x, y, n):
        """Extracts 2d-slice of size n at pos x, y in matrix m."""
        return [row[y * n: y * n + n] for row in m[x * n: x * n + n]]

    size = len(pattern)
    new_pattern = [list(range(size * m // n)) for _ in range(size * m // n)]
    for x in range(size // n):
        for y in range(size // n):
            result = rules[to_string(mslice(pattern, x, y, n))]
            for i, row in enumerate(to_matrix(result)):
                for j, col in enumerate(row):
                    new_pattern[x * m + i][y * m + j] = col
    return new_pattern


pattern = [
    list('.#.'),
    list('..#'),
    list('###'),
]
data = (line.strip() for line in open('rules.dat'))
rules = {rule: result for rule, result in expand_rules(data)}
for _ in range(18):
    if len(pattern) % 2 == 0:
        pattern = enhance(pattern, 2, 3)
    else:
        pattern = enhance(pattern, 3, 4)

print(sum(line.count('#') for line in pattern))
