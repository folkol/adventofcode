programs = list('abcdefghijklmnop')


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

moves = open('moves.dat').read().split(',')
for move in moves:
    op = move[0]
    params = move[1:].split('/')

    dispatch[op](programs, *params)

print('Result:', ''.join(programs))
