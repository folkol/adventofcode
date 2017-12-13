import re
from itertools import count

rows = (re.findall('\d+', line) for line in open('layers.dat'))
layers = {int(k): int(v) for k, v in rows}


def scanner_pos(delay, step):
    def route_len():
        return 2 + (layers[step] - 2) * 2

    return (delay + step) % route_len()


for delay in count():
    for step in range(max(layers) + 1):
        if step in layers and scanner_pos(delay, step) == 0:
            break
    else:
        break

print(delay)
