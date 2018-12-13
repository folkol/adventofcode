from dataclasses import make_dataclass
from itertools import count

Cart = make_dataclass('Cart', ['direction', 'turn'])

tracks = {}
carts = {}
with open('tracks.dat') as f:
    for y, line in enumerate(f):
        for x, c in enumerate(line.strip('\n')):
            if c in '^v<>':
                carts[(x, y)] = Cart(c, 'left')
            tracks[(x, y)] = c.translate(str.maketrans('^v<>', '||--'))


def coordinate(t):
    (x, y), _ = t
    return y, x


velocity = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
}

turn = {
    ('+', '<', 'left'): ('v', 'straight'),
    ('+', '>', 'left'): ('^', 'straight'),
    ('+', '^', 'left'): ('<', 'straight'),
    ('+', 'v', 'left'): ('>', 'straight'),
    ('+', '<', 'straight'): ('<', 'right'),
    ('+', '>', 'straight'): ('>', 'right'),
    ('+', '^', 'straight'): ('^', 'right'),
    ('+', 'v', 'straight'): ('v', 'right'),
    ('+', '<', 'right'): ('^', 'left'),
    ('+', '>', 'right'): ('v', 'left'),
    ('+', '^', 'right'): ('>', 'left'),
    ('+', 'v', 'right'): ('<', 'left'),

    ('/', '<', 'left'): ('v', 'left'),
    ('/', '>', 'left'): ('^', 'left'),
    ('/', '^', 'left'): ('>', 'left'),
    ('/', 'v', 'left'): ('<', 'left'),
    ('/', '<', 'straight'): ('v', 'straight'),
    ('/', '>', 'straight'): ('^', 'straight'),
    ('/', '^', 'straight'): ('>', 'straight'),
    ('/', 'v', 'straight'): ('<', 'straight'),
    ('/', '<', 'right'): ('v', 'right'),
    ('/', '>', 'right'): ('^', 'right'),
    ('/', '^', 'right'): ('>', 'right'),
    ('/', 'v', 'right'): ('<', 'right'),

    ('\\', '<', 'left'): ('^', 'left'),
    ('\\', '>', 'left'): ('v', 'left'),
    ('\\', '^', 'left'): ('<', 'left'),
    ('\\', 'v', 'left'): ('>', 'left'),
    ('\\', '<', 'straight'): ('^', 'straight'),
    ('\\', '>', 'straight'): ('v', 'straight'),
    ('\\', '^', 'straight'): ('<', 'straight'),
    ('\\', 'v', 'straight'): ('>', 'straight'),
    ('\\', '<', 'right'): ('^', 'right'),
    ('\\', '>', 'right'): ('v', 'right'),
    ('\\', '^', 'right'): ('<', 'right'),
    ('\\', 'v', 'right'): ('>', 'right'),
}

for tick in count():
    broken_carts = []
    for (x, y), cart in sorted(carts.items(), key=coordinate):
        if (x, y) in broken_carts:
            continue
        dx, dy = velocity[cart.direction]
        next_x, next_y = x + dx, y + dy
        if (next_x, next_y) in carts:
            # Crash!
            broken_carts.append((next_x, next_y))
            broken_carts.append((x, y))
            continue
        del carts[(x, y)]
        x, y = next_x, next_y
        carts[(x, y)] = cart
        position = ((tracks[(x, y)]), cart.direction, cart.turn)
        cart.direction, cart.turn = turn.get(position, (cart.direction, cart.turn))
    for x, y in broken_carts:
        del carts[(x, y)]
    if len(carts) == 1:
        x, y = next(iter(carts))
        print(f'The sole survivor stands tall at {x}, {y}!')
        break
