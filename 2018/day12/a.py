with open('plants.dat') as f:
    line = next(f)
    initial_state = [c == '#' for c in line.split()[2]]
    _ = next(f)
    rules = {}
    for line in f:
        configuration, _, result = line.split()
        rule = tuple(x == '#' for x in configuration)
        rules[rule] = result == '#'

        print(rule, '=>', result == '#')

N_GENERATIONS = 20
state = [False, False, False, False] * N_GENERATIONS + initial_state + [False, False, False, False] * N_GENERATIONS


def alive(n):
    t = tuple(state[n - 2:n + 3])
    return rules.get(t, False)


for generation in range(1, 20 + 1):
    state = [alive(i) for i, n in enumerate(state)]
    print(''.join('#' if n else '.' for n in state))

print(sum(i - 4 * N_GENERATIONS for i, n in enumerate(state) if n))