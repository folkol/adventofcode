WORD = "XMAS"
ORIENTATIONS = {
    "up": (1, 0),
    "down": (-1, 0),
    "left": (0, -1),
    "right": (0, 1),
    "major": (1, 1),
    "major_inv": (1, -1),
    "minor": (-1, 1),
    "minor_inv": (-1, -1),
}

with open("input.dat") as f:
    cells = {(x, y): c for (y, row) in enumerate(f) for (x, c) in enumerate(row)}


def word_match(x, y, dx, dy):
    return all(cells.get((x + n * dx, y + n * dy)) == c for (n, c) in enumerate(WORD))


def num_words_here(x, y):
    return sum(word_match(x, y, dx, dy) for dx, dy in ORIENTATIONS.values())


print(sum(num_words_here(x, y) for x, y in cells))
