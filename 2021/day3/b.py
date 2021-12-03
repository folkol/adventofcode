from collections import Counter
from itertools import count


def find_rating(xs, name):
    xs = list(xs)
    for bit in count():
        digits = Counter(x[bit] for x in xs)

        if name == 'oxygen':
            digit, frequency = digits.most_common()[0]
            keep = '1' if digits['0'] == digits['1'] else digit
        elif name == 'scrubber':
            digit, frequency = digits.most_common()[-1]
            keep = '0' if digits['0'] == digits['1'] else digit
        else:
            raise ValueError('Unknown rating name: ' + name)

        xs = [x for x in xs if x[bit] == keep]
        if len(xs) == 1:
            return int(xs[0], 2)


with open('input.dat') as f:
    report = [line.rstrip() for line in f]

print(find_rating(report, 'oxygen') * find_rating(report, 'scrubber'))
