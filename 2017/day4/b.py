"""Counts passphrases as defined by https://adventofcode.com/2017/day/4."""
import fileinput
from collections import Counter
from itertools import permutations


def valid_passphrase(passphrase):
    def is_anagram(word1, word2):
        return sorted(word1) == sorted(word2)

    cardinalities = Counter(passphrase)
    no_duplicates = all(cardinality == 1 for cardinality in cardinalities.values())
    words = cardinalities.keys()
    no_anarams = not any(is_anagram(word1, word2) for word1, word2 in permutations(words, r=2))

    return no_duplicates and no_anarams


phrases = (Counter(line.split()) for line in fileinput.input())
print(sum(1 for phrase in phrases if valid_passphrase(phrase)))
