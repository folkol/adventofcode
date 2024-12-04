SHAPES = [
    ['M.S', '.A.', 'M.S'],
    ['S.S', '.A.', 'M.M'],
    ['M.M', '.A.', 'S.S'],
    ['S.M', '.A.', 'S.M'],
]
OFFSETS = [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)]

with open("input.dat") as f:
    cells = {(x, y): c for (y, row) in enumerate(f) for (x, c) in enumerate(row)}


def shape_matches_here(x, y, shape):
    return all(cells.get((x - i, y - j)) == shape[1 - j][1 - i] for i, j in OFFSETS)


def num_words_here(x, y):
    return sum(shape_matches_here(x, y, shape) for shape in SHAPES)


print(sum(num_words_here(x, y) for x, y in cells))
