from sys import stdin

inside_garbage = False
garbage_count = 0
chars = iter(stdin.read())
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

print(garbage_count)
