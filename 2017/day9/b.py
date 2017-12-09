def as_chars(f):
    while True:
        c = f.read(1)
        if len(c) == 0:
            break
        yield c


depth = 0
score = 0
inside_garbage = False
garbage_count = 0
chars = as_chars(open('stream.dat'))
for char in chars:
    if char == '!':
        next(chars)
        continue

    if not inside_garbage and char == '<':
        inside_garbage = True
    elif inside_garbage:
        if char == '>':
            inside_garbage = False
        else:
            garbage_count += 1
    elif char == '{':
        depth += 1
    elif char == '}':
        score += depth
        depth -= 1

print(garbage_count)
