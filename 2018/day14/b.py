N = [8, 4, 6, 6, 0, 1]
scores = [3, 7]

elf1, elf2 = 0, 1
while True:
    ds = (int(n) for n in str(scores[elf1] + scores[elf2]))
    for d in ds:
        scores.append(d)
        if scores[-6:] == N:
            print('Found it @', len(scores) - 6)
            break
    elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
    elf2 = (elf2 + 1 + scores[elf2]) % len(scores)
