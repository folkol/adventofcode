def as_chars(f):
    while True:
        c = f.read(1)
        if len(c) == 0:
            break
        yield c


depth = 0
score = 0
prev = None
is_garbage = False
for char in as_chars(open('stream.dat')):
    if prev == '!':
        prev = None
        continue

    if char == '<':
        is_garbage = True
    elif is_garbage:
        if char == '>':
            is_garbage = False
    elif char == '{':
        depth += 1
    elif char == '}':
        score += depth
        depth -= 1

    prev = char

print(score)
