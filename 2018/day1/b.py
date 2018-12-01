import fileinput
from itertools import cycle

seen = set()
frequency = 0
terms = (int(term) for term in fileinput.input())
for i, delta in enumerate(cycle(terms)):
    frequency += delta
    if frequency in seen:
        print(f'Frequency {frequency} repeats with a period of {i}.')
        break
    seen.add(frequency)
