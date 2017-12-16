from itertools import count

N = 1_000_000_000
lineup = list('abcdefghijklmnop')
positions = lineup[:]
moves = open('moves.dat').read().split(',')


def spin(xs, i):
    i = int(i)
    xs[:] = xs[-i:] + xs[:-i]


def exchange(xs, a, b):
    i, j = int(a), int(b)
    xs[i], xs[j] = xs[j], xs[i]


def partner(xs, a, b):
    i, j = xs.index(a), xs.index(b)
    exchange(xs, i, j)


dispatch = {
    's': spin,
    'x': exchange,
    'p': partner
}


def dance():
    for move in moves:
        op = move[0]
        params = move[1:].split('/')
        dispatch[op](positions, *params)


for cycle_len in count(start=1):
    dance()
    if positions == lineup:
        break

for _ in range(N % cycle_len):
    dance()

print(''.join(positions))
