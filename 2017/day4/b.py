"""Counts passphrases as defined by https://adventofcode.com/2017/day/4."""
import fileinput
from itertools import permutations


def valid_passphrase(passphrase):
    def is_anagram(word1, word2):
        return sorted(word1) == sorted(word2)

    return not any(is_anagram(word1, word2) for word1, word2 in permutations(passphrase, r=2))


phrases = (line.split() for line in fileinput.input())
print(sum(1 for phrase in phrases if valid_passphrase(phrase)))
