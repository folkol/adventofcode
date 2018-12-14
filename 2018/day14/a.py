N = 846601
scores = [3, 7]

elf1, elf2 = 0, 1
while len(scores) < (N + 10):
    scores.extend(int(n) for n in str(scores[elf1] + scores[elf2]))
    elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
    elf2 = (elf2 + 1 + scores[elf2]) % len(scores)

print(*scores[N:N + 10], sep='')
