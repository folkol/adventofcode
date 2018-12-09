from collections import defaultdict
from itertools import cycle

NUM_PLAYERS = 458
NUM_MARBLES = 72019

marbles = iter(range(NUM_MARBLES + 1))
circle = [next(marbles)]
current = 0
players = list(range(1, NUM_PLAYERS + 1))
score = defaultdict(int)

for marble, player in zip(marbles, cycle(players)):
    if marble % 23 == 0:
        score[player] += marble
        i = (current - 7) % len(circle)
        score[player] += circle[i]
        del circle[i]
        current = i % len(circle)
    else:
        i = (current + 1) % len(circle)
        current = i + 1
        circle.insert(current, marble)
print(max(score.values()))
