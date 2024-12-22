with open('input.dat') as f:
    towels, designs = f.read().split('\n\n')
    towels = towels.split(', ')
    designs = designs.splitlines()


def is_possible(design, i=0):
    if i == len(design):
        return True
    for towel in towels:
        if design[i:].startswith(towel) and is_possible(design, i + len(towel)):
            return True
    return False


print(sum(is_possible(design) for design in designs))
