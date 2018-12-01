import fileinput
from itertools import cycle

seen = set()
frequency = 0
for term in cycle(int(term) for term in fileinput.input()):
    frequency += int(term)
    if frequency in seen:
        print('Repeated frequency:', frequency)
        break
    seen.add(frequency)
