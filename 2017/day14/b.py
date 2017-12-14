from functools import reduce
from itertools import product
from operator import xor

PADDING = [17, 31, 73, 47, 23]
SEED = 'amgozmfv'
NUM_ROWS = 128
NUM_COLS = 128
UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, +1)


def knot_hash(s):
    """Knot hash algorithm, stolen from day 10."""
    def rotate(lst, i):
        """Rotates the list lst i steps to the left."""
        lst[:] = lst[i:] + lst[:i]

    lengths = list(map(ord, s)) + PADDING
    xs = list(range(256))
    pos, skip = 0, 0
    for r in range(64):
        for length in lengths:
            rotate(xs, pos)
            xs[:length] = reversed(xs[:length])
            rotate(xs, -pos)
            pos = (pos + length + skip) % len(xs)
            skip += 1

    def chunk(lst, i, size=16):
        """Extracts chunk #i from the given list."""
        return lst[i * size:i * size + size]

    dense_hash = (reduce(xor, chunk(xs, x)) for x in range(16))
    return ''.join(f'{x:08b}' for x in dense_hash)


def groups():
    """Produces all groups from the grid."""
    hashes = (knot_hash(f'{SEED}-{i}') for i in range(NUM_ROWS))
    used = {row: [int(n) for n in list(h)] for row, h in enumerate(hashes)}
    seen = []

    def extract_group(row, col):
        """Flood fills the group at row, col. Marks these squares as 0 in the process."""
        group = []

        def visit(i, j):
            """Recursively visits all adjacent, and used, squares."""
            coordinate = i, j
            if coordinate in seen:
                return

            if 0 <= i < NUM_ROWS and 0 <= j < NUM_COLS and used[i][j]:
                seen.append(coordinate)
                for di, dj in UP, DOWN, LEFT, RIGHT:
                    visit(i + di, j + dj)
                group.append(coordinate)
                used[i][j] = 0

        visit(row, col)
        return group

    for row, col in product(range(NUM_ROWS), range(NUM_COLS)):
        if used[row][col]:
            yield extract_group(row, col)


print(sum(1 for _ in groups()))
