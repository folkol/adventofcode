import re

rows = (re.findall('\d+', line) for line in open('layers.dat'))
layers = {int(k): int(v) for k, v in rows}
print(layers)

severity = 0
for pos in range(max(layers) + 1):
    if pos not in layers:
        continue
    n = layers[pos]
    scanner_pos = pos % (2 + (n - 2) * 2)
    if scanner_pos == 0:
        print(f'Caught at depth {pos}')
        severity += pos * n

print(severity)
