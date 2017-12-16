from itertools import count

N = 1_000_000_000
lineup = list('abcdefghijklmnop')
# lineup = list('abcde')
positions = lineup[:]
moves = open('moves.dat').read().split(',')


# moves = 's1,x3/4,pe/b'.split(',')


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

for cycle_len in count():
    move = moves[(cycle_len % len(moves))]

    before = ''.join(list(positions))

    op = move[0]
    params = move[1:].split('/')
    dispatch[op](positions, *params)

    print(f"{move:8} {before:18} -> {''.join(positions)}")
    if positions == list(lineup):
        break

# TODO: Cycles in number of dances, not in number of moves...
n_cycle_len = N % cycle_len
print(cycle_len, n_cycle_len)
for n in range(n_cycle_len):
    move = moves[n % len(moves)]

    op = move[0]
    params = move[1:].split('/')
    dispatch[op](positions, *params)

print(''.join(positions))  # fgjkobpdheinlmac


