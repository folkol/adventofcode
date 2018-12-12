with open('plants.dat') as f:
    line = next(f)
    initial_state = [c == '#' for c in line.split()[2]]
    _ = next(f)
    rules = {}
    for line in f:
        configuration, _, result = line.split()
        rule = tuple(x == '#' for x in configuration)
        rules[rule] = result == '#'
        # print(rule, '=>', result == '#')

N_GENERATIONS = 1000
state = [False, False, False, False] * N_GENERATIONS + initial_state + [False, False, False, False] * N_GENERATIONS


def alive(n):
    t = tuple(state[n - 2:n + 3])
    return rules.get(t, False)


previous = 0
previous_delta = 0
for generation in range(1, N_GENERATIONS + 1):
    state = [alive(i) for i, n in enumerate(state)]
    value = sum(i - 4 * N_GENERATIONS for i, n in enumerate(state) if n)
    delta = value - previous
    if delta == previous_delta:
        print('Converged, cheating...!')
        print(value + delta * (50000000000 - generation))
        break
    # print(''.join('#' if n else '.' for n in state))
    previous_delta = delta
    previous = value
