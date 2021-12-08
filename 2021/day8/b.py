from itertools import permutations

CHARS = 'abcdefg'


def s(signal):
    return tuple(sorted(signal))


digits = {
    s('abcefg'): 0,
    s('cf'): 1,
    s('acdeg'): 2,
    s('acdfg'): 3,
    s('bcdf'): 4,
    s('abdfg'): 5,
    s('abdefg'): 6,
    s('acf'): 7,
    s('abcdefg'): 8,
    s('abcdfg'): 9,
}

result = 0
with open('input.dat') as f:
    for line in f:
        patterns, outputs = [part.split() for part in line.split(' | ')]
        for permutation in permutations(CHARS):
            trans = str.maketrans(''.join(permutation), CHARS)
            segments = (s(p.translate(trans)) for p in patterns)
            if set(digits) == set(segments):
                values = {s(p): digits[s(p.translate(trans))] for p in patterns}
                output = sum(pos * values[s(o)] for pos, o in zip([1000, 100, 10, 1], outputs))
                result += output

print(result)
