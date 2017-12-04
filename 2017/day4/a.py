"""Counts passphrases as defined by https://adventofcode.com/2017/day/4."""
import fileinput
from collections import Counter


def valid_passphrase(passphrase):
    cardinalities = Counter(passphrase)
    return all(cardinality == 1 for cardinality in cardinalities.values())


phrases = (line.split() for line in fileinput.input())
print(sum(1 for phrase in phrases if valid_passphrase(phrase)))
