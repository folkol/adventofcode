xs = list(range(256))
lengths = (int(x) for x in '106,16,254,226,55,2,1,166,177,247,93,0,255,228,60,36'.split(","))

pos = 0
skip = 0
for length in lengths:
    xs = xs[pos:] + xs[:pos]  # Shift left
    xs[:length] = reversed(xs[:length])
    xs = xs[-pos:] + xs[:-pos]  # Shift right
    pos = (pos + length + skip) % len(xs)
    skip += 1

print(xs[0] * xs[1])
