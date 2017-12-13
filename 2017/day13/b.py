import re

rows = (re.findall('\d+', line) for line in open('layers.dat'))
layers = {int(k): int(v) for k, v in rows}
print(layers)

delay = 0
while True:
    severity = 0
    for pos in range(max(layers) + 1):
        if pos not in layers:
            continue
        n = layers[pos]
        scanner_pos = (delay + pos) % (2 + (n - 2) * 2)
        if scanner_pos == 0:
            # print(f'Caught at depth {pos}')
            severity = 1
    if severity == 0:
        print(f'Got through unharmed with a delay of {delay}')
        break
    delay += 1
