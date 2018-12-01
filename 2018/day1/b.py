import fileinput
from itertools import cycle

seen = set()
frequency = 0
for delta in cycle(int(term) for term in fileinput.input()):
    frequency += delta
    if frequency in seen:
        print('Repeated frequency:', frequency)
        break
    seen.add(frequency)
