inside_garbage = False
garbage_count = 0
data = iter(open('stream.dat').read())
for char in data:
    if char == '!':
        next(data)
        continue

    if not inside_garbage and char == '<':
        inside_garbage = True
    elif inside_garbage:
        if char == '>':
            inside_garbage = False
        else:
            garbage_count += 1

print(garbage_count)
