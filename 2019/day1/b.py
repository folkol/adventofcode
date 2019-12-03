def fuel(w):
    while (w := w // 3 - 2) > 0:
        yield w

with open('input.dat') as f:
    modules = [int(line) for line in f]

print(sum(part for module in modules for part in fuel(module)))  # 5162216