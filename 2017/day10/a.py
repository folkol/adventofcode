def rotate(lst, i):
    """Rotates the list lst i steps to the left."""
    lst[:] = lst[i:] + lst[:i]


lengths = (int(x) for x in '106,16,254,226,55,2,1,166,177,247,93,0,255,228,60,36'.split(","))

xs = list(range(256))
pos = 0
skip = 0
for length in lengths:
    rotate(xs, pos)
    xs[:length] = reversed(xs[:length])
    rotate(xs, -pos)
    pos = (pos + length + skip) % len(xs)
    skip += 1

print(xs[0] * xs[1])
