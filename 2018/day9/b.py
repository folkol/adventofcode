from collections import defaultdict
from itertools import cycle

NUM_PLAYERS = 458
NUM_MARBLES = 72019


class Node:
    def __init__(self, marble):
        self.prev = self
        self.next = self
        self.marble = marble

    def __repr__(self):
        return f'{self.prev.prev.marble} -> {self.prev.marble} -> [{self.marble}] -> {self.next.marble} -> {self.next.next.marble}'


class Circle:

    def __init__(self, marble):
        self.current = Node(marble)

    def place(self, marble):
        self.current = self.current.next
        node = Node(marble)
        node.prev = self.current
        node.next = self.current.next
        self.current.next.prev = node
        self.current.next = node
        self.current = self.current.next

    def remove(self):
        for _ in range(7):
            self.current = self.current.prev
        score = self.current.marble
        self.current.prev.next = self.current.next
        self.current.next.prev = self.current.prev
        self.current = self.current.next
        return score


marbles = iter(range(NUM_MARBLES + 1))
circle = Circle(next(marbles))
current = 0
players = list(range(1, NUM_PLAYERS + 1))
score = defaultdict(int)

for marble, player in zip(marbles, cycle(players)):
    if marble % 23 == 0:
        score[player] += marble
        score[player] += circle.remove()
    else:
        circle.place(marble)
print(max(score.values()))
