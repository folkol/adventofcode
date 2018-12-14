N = [8, 4, 6, 6, 0, 1]
scores = [3, 7]

elf1, elf2 = 0, 1
found = None
while not found:
    for d in (int(d) for d in str(scores[elf1] + scores[elf2])):
        scores.append(d)
        if scores[-len(N):] == N:
            found = len(scores) - len(N)
            break
    elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
    elf2 = (elf2 + 1 + scores[elf2]) % len(scores)

print('Found it at', found)
