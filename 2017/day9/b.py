from sys import stdin

inside_garbage = False
garbage_count = 0
chars = iter(stdin.read())
for char in chars:
    if char == '!':
        next(chars)
        continue

    if inside_garbage:
        if char == '>':
            inside_garbage = False
        else:
            garbage_count += 1
    elif char == '<':
        inside_garbage = True

print(garbage_count)
