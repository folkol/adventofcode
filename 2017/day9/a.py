from sys import stdin

depth = 0
score = 0
inside_garbage = False

chars = iter(stdin.read())  # TODO: Idiomatic way of streaming these?
for char in chars:
    if char == '!':
        # Skip skip skip! (https://www.youtube.com/watch?v=c8jbSoCbnns)
        next(chars)
        continue

    if inside_garbage:
        if char == '>':
            inside_garbage = False
    elif char == '<':
        inside_garbage = True
    elif char == '{':
        depth += 1
    elif char == '}':
        score += depth
        depth -= 1

print(score)
