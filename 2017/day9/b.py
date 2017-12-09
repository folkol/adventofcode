def as_chars(f):
    while True:
        c = f.read(1)
        if len(c) == 0:
            break
        yield c


depth = 0
score = 0
inside_garbage = False
chars = as_chars(open('stream.dat'))
for char in chars:
    if char == '!':
        next(chars)
        continue

    if char == '<':
        inside_garbage = True
    elif inside_garbage:
        if char == '>':
            inside_garbage = False
    elif char == '{':
        depth += 1
    elif char == '}':
        score += depth
        depth -= 1

print(score)
