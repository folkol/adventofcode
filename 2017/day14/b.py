from functools import reduce
from operator import xor

SEED = 'amgozmfv'
NUM_ROWS = 128
NUM_COLS = 128


def knot_hash(s):
    def rotate(lst, i):
        """Rotates the list lst i steps to the left."""
        lst[:] = lst[i:] + lst[:i]

    lengths = [ord(x) for x in s] + [17, 31, 73, 47, 23]

    xs = list(range(256))
    pos = 0
    skip = 0
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
    return ''.join(f'{x:08b}' for x in dense_hash)[:NUM_COLS]


def groups():
    hashes = (knot_hash(f'{SEED}-{i}') for i in range(NUM_ROWS))
    used = {row: [int(n) for n in list(hash)] for row, hash in enumerate(hashes)}

    seen = []

    def extract_group(row, col):
        group = []

        def visit(i, j):
            coordinate = i, j
            if not (0 <= i < NUM_ROWS):
                return
            if not (0 <= j < NUM_COLS):
                return
            if coordinate in seen:
                return
            seen.append(coordinate)

            if used[i][j]:
                group.append(coordinate)

                visit(i - 1, j)
                visit(i + 1, j)
                visit(i, j - 1)
                visit(i, j + 1)

        visit(row, col)
        for i, j in group:
            used[i][j] = 0

        return group

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if used[row][col]:
                yield extract_group(row, col)


print(sum(1 for _ in groups()))
