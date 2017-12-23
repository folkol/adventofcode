def to_matrix(s):
    """123/456/789 -> [[1,2,3],[4,5,6],[7,8,9]]"""
    return [list(row) for row in s.split('/')]


def to_string(m):
    """[[1,2,3],[4,5,6],[7,8,9]] -> 123/456/789"""
    return '/'.join(''.join(x) for x in m)


def symmetries(matrix):
    """Generates all elements of the dihedral group containing `matrix`."""

    def rotate(m):
        """Rotates the list of lists 90 degrees."""
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


data = (
    '../.# => ##./#../...',
    '.#./..#/### => #..#/..../..../#..#'
)


def expand_rules(data):
    for datum in data:
        rule, result = datum.split(' => ')
        for symmetry in symmetries(to_matrix(rule)):
            yield to_string(symmetry), result


pattern = [
    list('.#.'),
    list('..#'),
    list('###'),
]
data = (line.strip() for line in open('rules.dat'))
rules = {rule: result for rule, result in expand_rules(data)}
for _ in range(5):
    size = len(pattern)
    if len(pattern) % 2 == 0:
        new_pattern = [list(range(size * 3 // 2)) for _ in range(size * 3 // 2)]
        for x in range(size // 2):
            for y in range(size // 2):
                square = [pattern[x * 2][y * 2:y * 2 + 2],
                          pattern[x * 2 + 1][y * 2:y * 2 + 2]]
                result = rules[to_string(square)]
                for i, row in enumerate(to_matrix(result)):
                    for j, col in enumerate(row):
                        new_pattern[x * 3 + i][y * 3 + j] = col
        pattern = new_pattern
    else:
        new_pattern = [list(range(size * 4 // 3)) for _ in range(size * 4 // 3)]
        for x in range(size // 3):
            for y in range(size // 3):
                square = [pattern[x * 3][y * 3:y * 3 + 3],
                          pattern[x * 3 + 1][y * 3:y * 3 + 3],
                          pattern[x * 3 + 2][y * 3:y * 3 + 3]]
                result = rules[to_string(square)]
                for i, row in enumerate(to_matrix(result)):
                    for j, col in enumerate(row):
                        new_pattern[x * 4 + i][y * 4 + j] = col
        pattern = new_pattern

values = sum(line.count('#') for line in pattern)
assert values == 150, values
print(values)
