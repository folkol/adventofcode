from functools import cache

with open('input.dat') as f:
    towels, designs = f.read().split('\n\n')
    towels = towels.split(', ')
    designs = designs.splitlines()


def match_here(towel, design, i, l):
    if i + l > len(design):
        return False
    return all(c == design[i + j] for j, c in enumerate(towel))


@cache
def num_possible(design, i=0):
    if i == len(design):
        return 1
    return sum(
        num_possible(design, i + len(towel))
        for towel in towels
        if match_here(towel, design, i, len(towel))
    )


print(sum(num_possible(design) for design in designs))
